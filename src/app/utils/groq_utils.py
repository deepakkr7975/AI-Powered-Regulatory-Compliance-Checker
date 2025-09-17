import json
import re
import time
from groq import Groq

def safe_json_parse(content, clauses, start_id):
    try:
        return json.loads(content)
    except:
        try:
            content = re.sub(r"```(?:json)?", "", content).strip()
            match = re.search(r"\[.*\]", content, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except:
            pass
    return [
        {
            "Clause ID": i + start_id,
            "Contract Clause": cl,
            "Regulation": "Unknown",
            "Risk Level": "Unknown",
            "AI Analysis": "Failed to parse AI output."
        }
        for i, cl in enumerate(clauses)
    ]


def analyze_batch(groq_client, clauses, start_id, retries=3):
    """Analyze a batch of clauses with retries + fallback."""
    if not clauses:
        return []

    prompt = f"""
    You are a compliance AI assistant.
    Analyze the following contract clauses against GDPR, CCPA, and HIPAA.

    Return ONLY valid JSON.
    Format: [
      {{
        "Clause ID": <number>,
        "Contract Clause": "<text>",
        "Regulation": "<GDPR/CCPA/HIPAA/None>",
        "Risk Level": "<High/Medium/Low/None>",
        "AI Analysis": "<short explanation>"
      }}
    ]

    Clauses: {json.dumps([{"Clause ID": i+start_id, "Contract Clause": cl} for i, cl in enumerate(clauses)])}
    """

    models = ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"]

    for attempt in range(retries):
        for model in models:
            try:
                response = groq_client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1200,
                    temperature=0
                )
                content = response.choices[0].message.content
                return safe_json_parse(content, clauses, start_id)
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(2)  # backoff
                else:
                    return safe_json_parse("[]", clauses, start_id)
