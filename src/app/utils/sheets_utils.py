# sheets_utils.py
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from .config import SERVICE_ACCOUNT_FILE, SPREADSHEET_ID, SHEET_NAME

def get_worksheet():
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    gs_client = gspread.authorize(creds)
    return gs_client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

def write_to_sheets(worksheet, rows):
    worksheet.clear()
    worksheet.update(values=rows, range_name="A1")

def fetch_from_sheets() -> pd.DataFrame:
    """Fetch results from Google Sheets as DataFrame."""
    worksheet = get_worksheet()
    data = worksheet.get_all_values()
    if not data:
        return pd.DataFrame()
    headers, rows = data[0], data[1:]
    return pd.DataFrame(rows, columns=headers)
