import streamlit as st
import pandas as pd
from gemini_client import run_all_personas
from analyzer import analyze

st.set_page_config(page_title="RankSense AI — Gemini Edition", page_icon="🧠", layout="wide")

st.markdown("### 🧠 RankSense AI")
st.title("AEO Diagnostic Engine — Gemini Edition")

query = st.text_input("Enter product query")

if st.button("Analyze"):
    results = run_all_personas(query)
    analysis = analyze(results)

    st.subheader("Leaderboard")
    if analysis["frequency"]:
        df = pd.DataFrame(analysis["frequency"])
        st.dataframe(df)

    st.subheader("Insights")
    for i in analysis["insights"]:
        st.write("-", i)
