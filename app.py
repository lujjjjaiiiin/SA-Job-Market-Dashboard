# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Saudi Job Market Dashboard",
    layout="wide",
    page_icon="📊"
)

# =========================
# STYLE
# =========================
st.markdown("""
    <style>
        .main { background-color: #F7F9FC; }
        h1, h2, h3 { color: #1B4F72; }
    </style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.title("📊 Saudi Arabia Job Market Dashboard")
st.caption("Jadarat Dataset Analysis — Clean & Interactive Dashboard")

# =========================
# LOAD DATA (CACHED)
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("Jadarat.csv")
    df.columns = df.columns.str.strip()
    df = df.drop_duplicates()
    return df

df = load_data()

# =========================
# FEATURE ENGINEERING
# =========================
df.columns = df.columns.str.strip()

df["job_title"] = df["job_title"].astype(str)

TECH_PATTERN = r'data scientist|data analyst|software|developer|ai|machine learning|python|java|sql'

df["is_tech_job"] = df["job_title"].str.lower().str.contains(
    TECH_PATTERN,
    na=False
).astype(int)

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🔎 Filters")

# -----------------------
# CITY FILTER
# -----------------------
if "city" in df.columns:
    cities = st.sidebar.multiselect(
        "City",
        sorted(df["city"].dropna().unique())
    )
    if cities:
        df = df[df["city"].isin(cities)]

# -----------------------
# CONTRACT FILTER
# -----------------------
if "contract" in df.columns:
    contracts = st.sidebar.multiselect(
        "Contract Type",
        sorted(df["contract"].dropna().unique())
    )
    if contracts:
        df = df[df["contract"].isin(contracts)]

# -----------------------
# TECH / NON-TECH FILTER
# -----------------------
tech_filter = st.sidebar.radio(
    "Job Type",
    ["All", "Tech Only", "Non-Tech Only"]
)

if tech_filter == "Tech Only":
    df = df[df["is_tech_job"] == 1]

elif tech_filter == "Non-Tech Only":
    df = df[df["is_tech_job"] == 0]
# =========================
# KPI SECTION
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("📌 Total Jobs", f"{len(df):,}")
col2.metric("💻 Tech Jobs", f"{df['is_tech_job'].sum():,}")
col3.metric("📊 Tech %", f"{df['is_tech_job'].mean()*100:.1f}%")

st.divider()

# =========================
# TOP JOBS & CITIES
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top Job Titles")
    if "job_title" in df.columns:
        top_jobs = df["job_title"].value_counts().head(10)

        fig, ax = plt.subplots()
        top_jobs.sort_values().plot(kind="barh", ax=ax, color="#2E86C1")
        ax.set_xlabel("Count")
        ax.set_title("Top 10 Job Titles")

        st.pyplot(fig)

with col2:
    st.subheader("📍 Top Hiring Cities")
    if "city" in df.columns:
        top_cities = df["city"].value_counts().head(10)

        fig, ax = plt.subplots()
        top_cities.sort_values().plot(kind="barh", ax=ax, color="#E67E22")
        ax.set_xlabel("Count")
        ax.set_title("Top 10 Cities")

        st.pyplot(fig)

st.divider()

# =========================
# CONTRACT + SALARY
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Contract Type")
    if "contract" in df.columns:
        contract = df["contract"].value_counts()

        fig, ax = plt.subplots()
        ax.pie(contract, labels=contract.index, autopct="%1.1f%%")
        ax.set_title("Contract Distribution")

        st.pyplot(fig)

with col2:
    st.subheader("💰 Salary Distribution")
    if "Salary" in df.columns:
        salary = df["Salary"].dropna()

        fig, ax = plt.subplots()
        ax.hist(salary, bins=25, color="#28B463", edgecolor="white")
        ax.set_title("Salary Distribution")

        st.pyplot(fig)

st.divider()

# =========================
# TECH ANALYSIS
# =========================
st.subheader("💻 Tech vs Non-Tech Analysis")

col1, col2 = st.columns(2)

with col1:
    salary_comp = df.groupby("is_tech_job")["Salary"].mean()

    fig, ax = plt.subplots()
    salary_comp.plot(kind="bar", ax=ax, color=["#E74C3C", "#2E86C1"])
    ax.set_title("Average Salary Comparison")
    ax.set_xticklabels(["Non-Tech", "Tech"], rotation=0)

    st.pyplot(fig)

with col2:
    counts = df["is_tech_job"].value_counts()

    fig, ax = plt.subplots()
    ax.pie(counts, labels=["Non-Tech", "Tech"], autopct="%1.1f%%",
           colors=["#E74C3C", "#2E86C1"])

    ax.set_title("Job Type Share")

    st.pyplot(fig)

# =========================
# DATA TABLE
# =========================
st.subheader("📋 Data Preview")
st.dataframe(df, use_container_width=True)

# =========================
# DOWNLOAD
# =========================
csv = df.to_csv(index=False)

st.download_button(
    "📥 Download Filtered Data",
    data=csv,
    file_name="Jadarat_filtered.csv",
    mime="text/csv"
)
