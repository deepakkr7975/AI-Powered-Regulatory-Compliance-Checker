# score_section.py
import streamlit as st
import plotly.express as px
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
# --- Google Sheets Config ---
SERVICE_ACCOUNT_FILE ="/Applications/Deepakkr/SummerIntership/Ai_Compliance Checker/service_account.json"
SPREADSHEET_ID = "1ix5ZqRjc0zpW8uFe3_9WJebmY2REz-1b-DDduSgMooc"
SHEET_NAME ="GDPR"

def fetch_results_from_sheets():
    """Fetch latest compliance results directly from Google Sheets."""
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, 
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    client = gspread.authorize(creds)
    worksheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

def render_score_section():
    st.header("2. Compliance Score")

    results_df = fetch_results_from_sheets()

    if results_df.empty:
        st.warning("⚠️ No analysis results found in Google Sheets.")
        return

    # Assign weights for scoring
    risk_weights = {"Low": 1.0, "Medium": 0.5, "High": 0.0, "None": 1.0, "Unknown": 0.5}

    # Calculate earned points
    total_points = len(results_df)
    earned_points = sum(risk_weights.get(risk, 0.5) for risk in results_df["Risk Level"])
    compliance_score = round((earned_points / total_points) * 100, 2)

    # Pie chart
    fig_score = px.pie(
        names=["Compliant", "At Risk"],
        values=[compliance_score, 100 - compliance_score],
        hole=0.5,
        color_discrete_sequence=["#2ecc40", "#ff4136"],
    )

    fig_score.update_layout(
        annotations=[dict(
            text=f"{compliance_score}/100", 
            x=0.5, y=0.5, 
            font_size=22, 
            showarrow=False
        )]
    )

    st.plotly_chart(fig_score, use_container_width=True)
    st.markdown(f"**Current Compliance Score:** `{compliance_score}/100`")
