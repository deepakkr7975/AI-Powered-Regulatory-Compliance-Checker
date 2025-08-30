import PyPDF2
import json
import gspread
from groq import Groq
from google.oauth2.service_account import Credentials
from tqdm import tqdm
import re
import os
from dotenv import load_dotenv


load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME", "GDPR")


creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
gs_client = gspread.authorize(creds)
worksheet = gs_client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

def extract_clauses_from_pdf(pdf_path):
    clauses = []
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    
    clauses = [cl.strip() for cl in text.split(".") if len(cl.split()) > 5]
    return clauses

groq_client = Groq(api_key=GROQ_API_KEY)
def safe_json_parse(content, clauses, start_id):
    """
    Extract JSON from AI response safely.
    """
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
def analyze_batch(clauses, start_id):
    """
    Analyze a batch of clauses in one Groq API call.
    """
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
        model="llama-3.1-8b-instant",   
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1200,
        temperature=0
    )

    content = response.choices[0].message.content
    return safe_json_parse(content, clauses, start_id)
def process_pdf_to_sheets(pdf_path, batch_size=5):
    clauses = extract_clauses_from_pdf(pdf_path)

    rows = [["Clause ID", "Contract Clause", "Regulation", "Risk Level", "AI Analysis"]]

    num_batches = (len(clauses) + batch_size - 1) // batch_size

    for i in tqdm(range(0, len(clauses), batch_size), desc="Processing Batches", total=num_batches):
        batch = clauses[i:i+batch_size]
        results = analyze_batch(batch, i+1)

        for res in results:
            rows.append([
                res["Clause ID"],
                res["Contract Clause"],
                res["Regulation"],
                res["Risk Level"],
                res["AI Analysis"]
            ])

    worksheet.clear()
    worksheet.update(values=rows, range_name="A1")  

def run_milestone1(pdf_path: str):
    """
    Runs the full Milestone 1 task:
    - Extracts text from a PDF
    - Updates a Google Sheet with a completion message
    """

    print("Running Milestone 1 Task...")
    
    process_pdf_to_sheets(pdf_path,batch_size=5)
    
    print("Task Completed and results written to Google Sheets")

    
    

    
    

    
