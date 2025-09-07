
import os
import gspread
from tqdm import tqdm
from google.oauth2.service_account import Credentials
from app.utils.pdf_utils import extract_clauses_from_pdf
from app.utils.groq_utils import analyze_batch
from app.utils.validation_utils import validate_results
from groq import Groq

def process_pdf_to_sheets(pdf_text, semantic=False, batch_size=5):
    
    creds = Credentials.from_service_account_file(
        os.getenv("SERVICE_ACCOUNT_FILE"),
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    gs_client = gspread.authorize(creds)
    worksheet = gs_client.open_by_key(os.getenv("SPREADSHEET_ID")).worksheet(os.getenv("SHEET_NAME", "GDPR"))
    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    
    clauses = extract_clauses_from_pdf(pdf_text, semantic=semantic)
    rows = [["Clause ID", "Contract Clause", "Regulation", "Risk Level", "AI Analysis"]]

    
    for i in tqdm(range(0, len(clauses), batch_size), desc="Processing Batches"):
        batch = clauses[i:i+batch_size]
        raw_results = analyze_batch(groq_client, batch, i+1)
        results = validate_results(raw_results, i+1, batch)

        for res in results:
            rows.append([res["Clause ID"], res["Contract Clause"], res["Regulation"], res["Risk Level"], res["AI Analysis"]])

    worksheet.clear()
    worksheet.update("A1", rows)
