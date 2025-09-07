import json
import re
from groq import Groq
from .config import GROQ_API_KEY

groq_client = Groq(api_key=GROQ_API_KEY)

def safe_json_parse(content, clauses, start_id):
    try:
        return json.loads(content)
    except:
        try:
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

def analyze_batch(groq_client, clauses, start_id):
    prompt = f"""
    You are a compliance AI assistant.
    Analyze the following contract clauses against GDPR, CCPA, and HIPAA.
    

    Return ONLY valid JSON (no markdown, no explanations outside JSON).
    Format strictly as a JSON list of objects like this:
    [
      {{
        "Clause ID": <number>,
        "Contract Clause": "<text>",
        "Regulation": "<GDPR/CCPA/HIPAA/None>",
        "Risk Level": "<High/Medium/Low/None>",
        "AI Analysis": "<short explanation>"
      }}
    ]

    Clauses to analyze:
    {json.dumps([{"Clause ID": i+start_id, "Contract Clause": cl} for i, cl in enumerate(clauses)])}
    """

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1200,
        temperature=0
    )

    content = response.choices[0].message.content
    return safe_json_parse(content, clauses, start_id)

