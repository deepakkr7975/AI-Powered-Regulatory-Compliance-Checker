import streamlit as st
from ui.upload_section import render_upload_section
from ui.risk_section import render_risk_section
from ui.summary_section import render_summary_section
from ui.dashboard import render_dashboard_section
import sys
import os
sys.path.append(os.path.dirname(__file__))

st.set_page_config(
    page_title="AI Contract Compliance Dashboard",
    page_icon="📑",
    layout="wide"
)

st.sidebar.title("📂 Dashboard Menu")
analysis_type = st.sidebar.radio(
    "Select Section to View",
    [
        "Upload Contract",
        "Compliance Score",
        "Risk Analysis",
        "Summary & Insights"
    ]
)

st.title("⚖️ AI-Powered Regulatory Compliance Checker")

if analysis_type == "Upload Contract":
    render_upload_section()

elif analysis_type == "Risk Analysis":
    render_risk_section()
    
elif analysis_type == "Summary & Insights":
    render_summary_section()
    
elif analysis_type == "Integrations":
    st.info("Coming soon — Google Sheets / Slack integration.")

elif analysis_type == "Compliance Score":
    render_dashboard_section()
