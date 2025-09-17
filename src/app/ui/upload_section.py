# upload_section.py
import streamlit as st
from app.pipeline import process_pdf_to_sheets
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets config
SERVICE_ACCOUNT_FILE ="/Applications/Deepakkr/SummerIntership/Ai_Compliance Checker/service_account.json"
SPREADSHEET_ID = "1ix5ZqRjc0zpW8uFe3_9WJebmY2REz-1b-DDduSgMooc"
SHEET_NAME ="GDPR"

def save_to_sheets(df):
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, 
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    client = gspread.authorize(creds)
    worksheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

    worksheet.clear()  # clear old results
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())  # write new results

def render_upload_section():
    st.header("1. Upload Your Contract File")

    uploaded_file = st.file_uploader("Choose a .pdf or .docx file", type=["pdf", "docx"])

    if uploaded_file is not None:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        st.write(f"**Type:** {uploaded_file.type}")
        st.write(f"**Size:** {round(uploaded_file.size / 1024, 2)} KB")

        if st.button("🚀 Run Compliance Analysis"):
            with st.spinner("Analyzing contract... Please wait ⏳"):
                results_df = process_pdf_to_sheets(uploaded_file, mode="dataframe", batch_size=5)
                
                # 🔹 Save to Sheets instead of only session state
                save_to_sheets(results_df)

            st.success("✅ Analysis complete! Data is now available in Google Sheets.")

            st.subheader("🔍 Preview of Analyzed Clauses")
            st.dataframe(results_df.head(10), use_container_width=True)
    else:
        st.info("📂 Please upload a contract file to begin compliance checks.")
