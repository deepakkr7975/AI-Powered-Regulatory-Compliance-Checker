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
