import streamlit as st
import gspread
import os
from datetime import datetime
from google.oauth2.service_account import Credentials

# =========================
# GOOGLE SHEETS SETUP (ROBUST)
# =========================

@st.cache_resource
def init_gsheets():

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # load credentials
    creds = Credentials.from_service_account_file(
        "credentials.json",
        scopes=scope
    )

    # DEBUG ONLY
    st.write("SERVICE ACCOUNT EMAIL:", creds.service_account_email)
    st.write("PROJECT ID:", getattr(creds, "project_id", "N/A"))
    st.write("CREDENTIAL FILE FOUND:", os.path.exists("credentials.json"))

    client = gspread.authorize(creds)

    spreadsheet_id = "1djMtdtozoTyQDOKbgoN0neCF2Cqwn6WCiYvsUM2ALRI"

    # =========================
    # IMPORTANT FIX: avoid open_by_key issue fallback
    # =========================
    try:
        sheet = client.open_by_key(spreadsheet_id).sheet1
    except Exception as e:
        st.error("Google Sheets connection failed at open_by_key stage.")
        raise e

    return sheet


sheet = init_gsheets()

# =========================
# UI
# =========================

st.title("Public Economics CBT")

name = st.text_input("Student Name")
nim = st.text_input("NIM")

class_name = st.selectbox(
    "Class",
    ["Class A", "Class B", "Class C"]
)

# =========================
# STATE
# =========================

if "started" not in st.session_state:
    st.session_state.started = False

if st.button("Start Exam"):
    if not name or not nim:
        st.warning("Fill identity first.")
    else:
        st.session_state.started = True

# =========================
# QUESTIONS
# =========================

if st.session_state.started:

    q1 = st.radio("1. Public good?", [
        "Private good",
        "Non-rival and non-excludable",
        "Luxury good",
        "Inferior good"
    ], key="q1")

    q2 = st.radio("2. Taxation objective?", [
        "Increase inequality",
        "Finance public expenditure",
        "Reduce production",
        "Eliminate trade"
    ], key="q2")

    q3 = st.radio("3. Externality occurs when?", [
        "Markets are perfect",
        "Third parties are affected",
        "Taxes disappear",
        "Inflation rises"
    ], key="q3")

    q4 = st.radio("4. Fiscal policy?", [
        "Government spending and taxation",
        "Monetary policy",
        "Trade policy",
        "Exchange rate policy"
    ], key="q4")

    # =========================
    # SUBMIT
    # =========================

    if st.button("Submit"):

        score = 0

        if q1 == "Non-rival and non-excludable":
            score += 25
        if q2 == "Finance public expenditure":
            score += 25
        if q3 == "Third parties are affected":
            score += 25
        if q4 == "Government spending and taxation":
            score += 25

        st.success(f"Final Score = {score}")

        try:
            sheet.append_row([
                str(datetime.now()),
                nim,
                name,
                class_name,
                score
            ])
            st.info("Saved to Google Sheets.")
        except Exception as e:
            st.error("Write failed")
            st.exception(e)
