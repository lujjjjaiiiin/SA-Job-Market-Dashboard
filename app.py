# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px

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

TECH_PATTERN = r'\bdata scientist\b|\bdata analyst\b|\bsoftware\b|\bdeveloper\b|\bai\b|\bmachine learning\b|\bpython\b|\bjava\b|\bsql\b'

df["is_tech_job"] = (
    df["job_title"]
    .str.lower()
    .str.contains(TECH_PATTERN, na=False)
    .astype(int)
)

# =========================
# STYLE
# =========================
st.markdown("""
<style>
.main {
    background: linear-gradient(180deg,#0B1220,#0F172A);
}

h1, h2, h3 {
    color: #22C55E;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#052e16,#14532D);
    border-right: 2px solid #22C55E;
}

[data-testid="stSidebar"] * {
    color: white !important;
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
<p style="color:#A7F3D0;margin:0;">Vision 2030 • Jadarat Dataset</p>
</div>

</div>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR FILTERS
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
# KPI METRICS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Total Jobs", len(df))
col2.metric("Tech Jobs", df["is_tech_job"].sum())
col3.metric("Tech %", f"{df['is_tech_job'].mean()*100:.1f}%")

st.divider()

# =========================
# INSIGHTS
# =========================

st.subheader("📈 Key Insights")

top_city = df["city"].value_counts().idxmax()
top_city_count = df["city"].value_counts().max()

top_job = df["job_title"].value_counts().idxmax()
top_job_count = df["job_title"].value_counts().max()

avg_salary = df["Salary"].mean()

col1, col2, col3 = st.columns(3)

col1.success(
    f"📍 {top_city} has the highest number of job postings ({top_city_count:,})."
)

col2.info(
    f"💼 Most demanded role is '{top_job}' with {top_job_count:,} postings."
)

col3.warning(
    f"💰 Average salary is approximately {avg_salary:,.0f} SAR."
)

# =========================
# TOP JOBS (HOVER)
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Job Titles")

    top_jobs = df["job_title"].value_counts().head(10).reset_index()
    top_jobs.columns = ["job_title", "count"]

    fig = px.bar(
        top_jobs,
        x="count",
        y="job_title",
        orientation="h",
        text="count"
    )

    fig.update_traces(marker_color="#22C55E")
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Top Cities")

    top_cities = df["city"].value_counts().head(10).reset_index()
    top_cities.columns = ["city", "count"]

    fig = px.bar(
        top_cities,
        x="count",
        y="city",
        orientation="h",
        text="count"
    )

    fig.update_traces(marker_color="#16A34A")
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# =========================
# CONTRACT PIE (HOVER)
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Contract Type")

    contract = df["contract"].value_counts().reset_index()
    contract.columns = ["contract", "count"]

    fig = px.pie(
        contract,
        names="contract",
        values="count",
        hole=0.4
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Salary Distribution")

    fig = px.histogram(
        df,
        x="Salary",
        nbins=25
    )

    fig.update_traces(marker_color="#22C55E")

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# =========================
# TECH VS NON TECH
# =========================
st.subheader("Tech vs Non-Tech (Average Salary)")

salary_comp = df.groupby("is_tech_job")["Salary"].mean().reset_index()
salary_comp["type"] = salary_comp["is_tech_job"].map({0: "Non-Tech", 1: "Tech"})

fig = px.bar(
    salary_comp,
    x="type",
    y="Salary",
    text="Salary"
)

fig.update_traces(marker_color=["#EF4444", "#22C55E"])
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="white"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# DATA PREVIEW
# =========================
st.subheader("Data Preview")
st.dataframe(df, use_container_width=True)

# =========================
# DOWNLOAD
# =========================
st.download_button(
    "📥 Download Data",
    df.to_csv(index=False),
    "Jadarat_filtered.csv",
    "text/csv"
)
