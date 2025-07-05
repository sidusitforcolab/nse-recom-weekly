import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="NSE Weekly Recommender", layout="wide")
st.title("📈 Weekly NSE Stock Picks")

csv_path = "output/weekly_top_stocks.csv"

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    st.success("Latest picks loaded successfully!")
    st.dataframe(df)
else:
    st.warning("No data yet. Run the workflow or check GitHub Actions.")