import streamlit as st
import gspread
import os
from datetime import datetime
from google.oauth2.service_account import Credentials

@st.cache_resource
def init_gsheets():

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_file(
        "credentials.json",
        scopes=scope
    )

    client = gspread.authorize(creds)

    st.write("SERVICE ACCOUNT:", creds.service_account_email)
    st.write("FILE EXISTS:", os.path.exists("credentials.json"))

    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1djMtdtozoTyQDOKbgoN0neCF2Cqwn6WCiYvsUM2ALRI/edit"

    try:
        sheet = client.open_by_url(spreadsheet_url).sheet1
    except Exception as e:
        st.error("Failed to open spreadsheet")
        raise e

    return sheet

sheet = init_gsheets()
