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
    page_icon="🇸🇦"
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("Jadarat.csv")
    df.columns = df.columns.str.strip()
    df = df.drop_duplicates()
    return df

df = load_data()

if df.empty:
    st.error("Dataset is empty")
    st.stop()

# =========================
# FEATURE ENGINEERING
# =========================
df["job_title"] = df["job_title"].astype(str)

TECH_PATTERN = r'data scientist|data analyst|software|developer|ai|machine learning|python|java|sql'

df["is_tech_job"] = (
    df["job_title"]
    .str.lower()
    .str.contains(TECH_PATTERN, na=False)
    .astype(int)
)

# =========================
# CSS (CLEAN + GREEN THEME)
# =========================
st.markdown("""
<style>

.main {
    background: linear-gradient(180deg,#0B1220,#0F172A);
}

h1, h2, h3 {
    color: #22C55E;
}

[data-testid="stMetric"] {
    background: rgba(34,197,94,0.08);
    border-radius: 12px;
    padding: 10px;
    border: 1px solid rgba(34,197,94,0.25);
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("""
<div style="
    background: linear-gradient(135deg,#0B1220,#14532D);
    padding:20px;
    border-radius:15px;
    display:flex;
    align-items:center;
    gap:15px;
">

<img src="https://upload.wikimedia.org/wikipedia/commons/0/0d/Flag_of_Saudi_Arabia.svg" width="60">

<div>
<h1 style="color:#22C55E;margin:0;">Saudi Arabia Job Market Dashboard</h1>
<p style="color:#A7F3D0;margin:0;">🇸🇦 Vision 2030 • Jadarat Dataset</p>
</div>

</div>
""", unsafe_allow_html=True)

# =========================
# FILTERS
# =========================
st.sidebar.header("🔎 Filters")

if "city" in df.columns:
    cities = st.sidebar.multiselect("City", sorted(df["city"].dropna().unique()))
    if cities:
        df = df[df["city"].isin(cities)]

if "contract" in df.columns:
    contracts = st.sidebar.multiselect("Contract Type", sorted(df["contract"].dropna().unique()))
    if contracts:
        df = df[df["contract"].isin(contracts)]

tech_filter = st.sidebar.radio("Job Type", ["All", "Tech Only", "Non-Tech Only"])

if tech_filter == "Tech Only":
    df = df[df["is_tech_job"] == 1]
elif tech_filter == "Non-Tech Only":
    df = df[df["is_tech_job"] == 0]

if df.empty:
    st.warning("No data for selected filters")
    st.stop()

# =========================
# KPIs
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Total Jobs", len(df))
col2.metric("Tech Jobs", df["is_tech_job"].sum())
col3.metric("Tech %", f"{df['is_tech_job'].mean()*100:.1f}%")

st.divider()

# =========================
# TOP JOBS & CITIES
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Job Titles")
    top_jobs = df["job_title"].value_counts().head(10)

    fig, ax = plt.subplots()
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    top_jobs.sort_values().plot(kind="barh", ax=ax, color="#22C55E")

    ax.tick_params(colors="white")

    st.pyplot(fig)

with col2:
    st.subheader("Top Cities")
    top_cities = df["city"].value_counts().head(10)

    fig, ax = plt.subplots()
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    top_cities.sort_values().plot(kind="barh", ax=ax, color="#16A34A")

    ax.tick_params(colors="white")

    st.pyplot(fig)

st.divider()

# =========================
# CONTRACT + SALARY
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Contract Type")

    contract = df["contract"].value_counts()

    fig, ax = plt.subplots()
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    ax.pie(
        contract.values,
        labels=[str(i) for i in contract.index],
        autopct="%1.1f%%",
        colors=["#22C55E", "#EF4444"][:len(contract)],
        textprops={"color": "white"}
    )

    st.pyplot(fig)

with col2:
    st.subheader("Salary Distribution")

    salary = df["Salary"].dropna()

    fig, ax = plt.subplots()
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    ax.hist(salary, bins=25, color="#22C55E", edgecolor="white")

    ax.tick_params(colors="white")

    st.pyplot(fig)

st.divider()

# =========================
# TECH ANALYSIS (FIXED)
# =========================
st.subheader("Tech vs Non-Tech")

col1, col2 = st.columns(2)

with col1:
    salary_comp = df.groupby("is_tech_job")["Salary"].mean()

labels_map = {0: "Non-Tech", 1: "Tech"}

fig, ax = plt.subplots()
fig.patch.set_alpha(0)
ax.set_facecolor("none")

salary_comp.plot(kind="bar", ax=ax, color=["#EF4444", "#22C55E"])

ax.set_xticklabels(
    [labels_map[i] for i in salary_comp.index],
    rotation=0,
    color="white"
)

st.pyplot(fig)

with col2:
    counts = df["is_tech_job"].value_counts()

    labels = ["Non-Tech" if i == 0 else "Tech" for i in counts.index]

    fig, ax = plt.subplots()
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    ax.pie(
        counts.values,
        labels=labels,
        autopct="%1.1f%%",
        colors=["#EF4444", "#22C55E"][:len(counts)],
        textprops={"color": "white"}
    )

    st.pyplot(fig)

# =========================
# TABLE
# =========================
st.subheader("Data Preview")
st.dataframe(df, use_container_width=True)

# =========================
# DOWNLOAD
# =========================
st.download_button(
    "Download CSV",
    df.to_csv(index=False),
    "Jadarat_filtered.csv",
    "text/csv"
)
