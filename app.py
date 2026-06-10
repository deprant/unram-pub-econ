import streamlit as st
import gspread
import os
from datetime import datetime
from google.oauth2.service_account import Credentials

# =========================
# CONFIG GOOGLE SHEETS
# =========================

SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1djMtdtozoTyQDOKbgoN0neCF2Cqwn6WCiYvsUM2ALRI/edit"

@st.cache_resource
def init_gsheets():

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # load service account
    creds = Credentials.from_service_account_file(
        "credentials.json",
        scopes=scope
    )

    client = gspread.authorize(creds)

    # DEBUG (aman)
    st.write("SERVICE ACCOUNT:", creds.service_account_email)
    st.write("FILE EXISTS:", os.path.exists("credentials.json"))

    # =========================
    # SAFE CONNECTION METHOD
    # =========================
    try:
        sheet = client.open_by_url(SPREADSHEET_URL).sheet1
    except Exception as e:
        st.error("FAILED TO CONNECT TO GOOGLE SHEETS")
        st.exception(e)
        return None

    return sheet


sheet = init_gsheets()

# =========================
# UI
# =========================

st.title("Public Economics CBT")

name = st.text_input("Student Name")
nim = st.text_input("NIM")

class_name = st.selectbox("Class", ["Class A", "Class B", "Class C"])

# =========================
# SESSION STATE
# =========================

if "started" not in st.session_state:
    st.session_state.started = False

if st.button("Start Exam"):
    if not name or not nim:
        st.warning("Please fill identity first")
    else:
        st.session_state.started = True

# =========================
# QUESTIONS
# =========================

if st.session_state.started:

    q1 = st.radio(
        "1. Public good is:",
        ["Private good", "Non-rival and non-excludable", "Luxury good", "Inferior good"],
        key="q1"
    )

    q2 = st.radio(
        "2. Main objective of taxation:",
        ["Increase inequality", "Finance public expenditure", "Reduce production", "Eliminate trade"],
        key="q2"
    )

    q3 = st.radio(
        "3. Externalities occur when:",
        ["Markets are perfect", "Third parties are affected", "Taxes disappear", "Inflation rises"],
        key="q3"
    )

    q4 = st.radio(
        "4. Fiscal policy is:",
        ["Government spending and taxation", "Monetary policy", "Trade policy", "Exchange rate policy"],
        key="q4"
    )

    # =========================
    # SUBMIT
    # =========================

    if st.button("Submit"):

        if sheet is None:
            st.error("Google Sheets is not connected.")
            st.stop()

        score = 0

        if q1 == "Non-rival and non-excludable":
            score += 25
        if q2 == "Finance public expenditure":
            score += 25
        if q3 == "Third parties are affected":
            score += 25
        if q4 == "Government spending and taxation":
            score += 25

        st.success(f"Final Score: {score}")

        try:
            sheet.append_row([
                str(datetime.now()),
                nim,
                name,
                class_name,
                score
            ])
            st.info("Saved to Google Sheets")
        except Exception as e:
            st.error("Failed to write to Google Sheets")
            st.exception(e)
