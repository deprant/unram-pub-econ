import streamlit as st
import gspread
import os
from datetime import datetime
from google.oauth2.service_account import Credentials

# =========================
# GOOGLE SHEETS SETUP
# =========================

@st.cache_resource
def init_gsheets():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # pastikan file ini ada di repo / Streamlit Cloud
    creds = Credentials.from_service_account_file(
        "credentials.json",
        scopes=scope
    )

    # DEBUG aman (tanpa attribute yang berisiko error)
    st.write("SERVICE ACCOUNT EMAIL:", creds.service_account_email)
    st.write("PROJECT ID:", getattr(creds, "project_id", "N/A"))
    st.write("Credentials file exists:", os.path.exists("credentials.json"))

    client = gspread.authorize(creds)

    spreadsheet_id = "1djMtdtozoTyQDOKbgoN0neCF2Cqwn6WCiYvsUM2ALRI"

    sheet = client.open_by_key(spreadsheet_id).sheet1

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
# SESSION STATE
# =========================

if "started" not in st.session_state:
    st.session_state.started = False

if st.button("Start Exam"):
    if not name or not nim:
        st.warning("Please fill Name and NIM first.")
    else:
        st.session_state.started = True

# =========================
# QUESTIONS
# =========================

if st.session_state.started:

    q1 = st.radio(
        "1. What is a public good?",
        [
            "Private good",
            "Non-rival and non-excludable",
            "Luxury good",
            "Inferior good"
        ],
        key="q1"
    )

    q2 = st.radio(
        "2. What is the main objective of taxation?",
        [
            "Increase inequality",
            "Finance public expenditure",
            "Reduce production",
            "Eliminate trade"
        ],
        key="q2"
    )

    q3 = st.radio(
        "3. Externalities occur when",
        [
            "Markets are perfect",
            "Third parties are affected",
            "Taxes disappear",
            "Inflation rises"
        ],
        key="q3"
    )

    q4 = st.radio(
        "4. What is fiscal policy?",
        [
            "Government spending and taxation",
            "Monetary policy",
            "Trade policy",
            "Exchange rate policy"
        ],
        key="q4"
    )

    # =========================
    # SUBMIT
    # =========================

    if st.button("Submit"):

        if not name or not nim:
            st.error("Incomplete identity")
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

        st.success(f"Final Score = {score}")

        # =========================
        # SAVE TO GOOGLE SHEETS
        # =========================

        try:
            sheet.append_row([
                str(datetime.now()),
                nim,
                name,
                class_name,
                score
            ])
            st.info("Saved successfully to Google Sheets.")
        except Exception as e:
            st.error("Failed to save to Google Sheets")
            st.exception(e)
