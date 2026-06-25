# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Saudi Job Market", layout="wide")

st.title("Saudi Arabia Job Market Dashboard")

# --------------------
# LOAD DATA (LOCAL FILE)
# --------------------
df = pd.read_csv("Jadarat.csv")

# تنظيف بسيط
df.columns = df.columns.str.strip()
df = df.drop_duplicates()

# --------------------
# FEATURE ENGINEERING
# --------------------
TECH_PATTERN = r'data scientist|data analyst|software|developer|ai|machine learning|python|java|sql'

df["is_tech_job"] = (
    df["job_title"]
    .str.lower()
    .str.contains(TECH_PATTERN, na=False)
    .astype(int)
)

# --------------------
# SIDEBAR FILTERS
# --------------------
st.sidebar.header("Filters")

if "city" in df.columns:
    cities = st.sidebar.multiselect("City", df["city"].dropna().unique())
    if cities:
        df = df[df["city"].isin(cities)]

# --------------------
# KPI
# --------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Jobs", len(df))
col2.metric("Tech Jobs", df["is_tech_job"].sum())
col3.metric("Tech %", f"{df['is_tech_job'].mean()*100:.1f}%")

# --------------------
# DOWNLOAD BUTTON (CORRECT WAY)
# --------------------
csv = df.to_csv(index=False)

st.download_button(
    "📥 Download Data",
    data=csv,
    file_name="Jadarat.csv",
    mime="text/csv"
)

# --------------------
# DATA PREVIEW
# --------------------
st.dataframe(df)
