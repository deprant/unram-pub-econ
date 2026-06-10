import streamlit as st
import pandas as pd
import gspread
from datetime import datetime
import os
st.write(os.listdir())
from google.oauth2.service_account import Credentials

# =========================
# GOOGLE SHEETS SETUP
# =========================

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=scope
)

client = gspread.authorize(creds)

sheet = client.open("CBT Public Economics Results").sheet1

# =========================
# UI IDENTITAS
# =========================

st.title("Public Economics CBT")

name = st.text_input("Student Name")
nim = st.text_input("NIM")

class_name = st.selectbox(
    "Class",
    ["Class A", "Class B", "Class C"]
)

# =========================
# STATE START EXAM
# =========================

if "started" not in st.session_state:
    st.session_state.started = False

if st.button("Start Exam"):
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

        sheet.append_row([
            str(datetime.now()),
            nim,
            name,
            class_name,
            score
        ])

        st.info("Result successfully recorded.")
