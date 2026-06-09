import streamlit as st
import pandas as pd
from datetime import datetime
import os

# =========================
# IDENTITAS MAHASISWA
# =========================

st.title("Public Economics CBT")

name = st.text_input("Student Name")

nim = st.text_input("NIM")

class_name = st.selectbox(
    "Class",
    [
        "Class A",
        "Class B",
        "Class C"
    ]
)

# =========================
# MULAI UJIAN
# =========================

if st.button("Start Exam"):
    st.session_state.started = True

# =========================
# SOAL UJIAN
# =========================

if "started" in st.session_state:

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
        # SIMPAN KE EXCEL
        # =========================

        result = pd.DataFrame({
            "Timestamp": [datetime.now()],
            "NIM": [nim],
            "Student Name": [name],
            "Class": [class_name],
            "Score": [score]
        })

        file_name = "cbt_results.xlsx"

        if os.path.exists(file_name):

            old_data = pd.read_excel(file_name)

            new_data = pd.concat(
                [old_data, result],
                ignore_index=True
            )

            new_data.to_excel(
                file_name,
                index=False
            )

        else:

            result.to_excel(
                file_name,
                index=False
            )

        st.info("Result saved successfully.")