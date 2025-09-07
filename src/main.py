import fitz
from app.pipeline import process_pdf_to_sheets

def read_pdf(path):
    text = ""
    doc = fitz.open(path)
    for page in doc:
        text += page.get_text()
    return text

def run_milestone1(pdf_path: str):
    print("Running...")
    pdf_text = read_pdf(pdf_path)
    process_pdf_to_sheets(pdf_text, semantic=False, batch_size=5)
    print("Task Completed. Results written to Google Sheets.")

if __name__ == "__main__":
    run_milestone1("test/edge_usa-meta_nsa_new_plcn_fully_executed_0.pdf")
