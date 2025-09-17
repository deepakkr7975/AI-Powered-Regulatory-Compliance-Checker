<<<<<<< HEAD
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
=======
import streamlit as st
from app.ui.upload_section import render_upload_section
from app.ui.score_section import render_score_section
from app.ui.risk_section import render_risk_section
import sys
import os
sys.path.append(os.path.dirname(__file__))  
st.set_page_config(page_title="AI Contract Compliance Dashboard", page_icon="📑", layout="wide")

st.sidebar.title("📂 Dashboard Menu")
analysis_type = st.sidebar.radio(
    "Select Section to View",
    [
        "Upload Contract",
        "Compliance Score",
        "Risk Analysis",
        "Regulatory Updates",
        "Alerts & Recommendations",
        "Integrations"
    ]
)

st.title("AI-Powered Regulatory Compliance Checker ")

if analysis_type == "Upload Contract":
    render_upload_section()

elif analysis_type == "Compliance Score":
    render_score_section()

elif analysis_type == "Risk Analysis":
    render_risk_section()

elif analysis_type == "Regulatory Updates":
    st.info("Coming soon — connect to live feeds.")

elif analysis_type == "Alerts & Recommendations":
    st.info("Coming soon — auto-generated alerts.")

elif analysis_type == "Integrations":
    st.info("Coming soon — Google Sheets / Slack integration.")
>>>>>>> 29c304c (Added UI and Improved data chunking)
