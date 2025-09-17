# pipeline.py
import pandas as pd
from tqdm import tqdm
from groq import Groq
import os
from dotenv import load_dotenv
from docx import Document  

from app.utils.pdf_utils import ingest_contract  
from app.utils.groq_utils import analyze_batch

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

groq_client = Groq(api_key=GROQ_API_KEY)


def read_docx(file_bytes):
    """Extract raw text from a DOCX file."""
    doc = Document(file_bytes)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])


def process_pdf_to_sheets(file_input, mode="dataframe", batch_size=5):
    """
    Process PDF or DOCX input (local path or Streamlit UploadedFile).
    Returns results as DataFrame.
    """

    if isinstance(file_input, str):
        # Local file path
        if file_input.lower().endswith(".docx"):
            text = read_docx(file_input)
        else:
            # Use ingestion for PDF
            clauses = ingest_contract(file_input)
    else:
        # Streamlit UploadedFile
        filename = file_input.name.lower()
        if filename.endswith(".docx"):
            text = read_docx(file_input)
            clauses = text.split("\n\n")  # simple docx split
        else:
            # Save uploaded file temporarily
            tmp_path = f"/tmp/{file_input.name}"
            with open(tmp_path, "wb") as f:
                f.write(file_input.read())
            clauses = ingest_contract(tmp_path)

    rows = []
    num_batches = (len(clauses) + batch_size - 1) // batch_size

    for i in tqdm(range(0, len(clauses), batch_size), desc="Processing Batches", total=num_batches):
        # For ingestion, each clause is a dict → use ["content"]
        batch = [clause["content"] if isinstance(clause, dict) else clause for clause in clauses[i:i+batch_size]]
        raw_results = analyze_batch(groq_client, batch, i + 1)
        rows.extend(raw_results)

    df = pd.DataFrame(rows)
    return df
