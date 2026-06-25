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

/* Fade-in animation */
@keyframes fadeIn {
    0% {opacity: 0; transform: translateY(-15px);}
    100% {opacity: 1; transform: translateY(0);}
}

/* Glow animation */
@keyframes glow {
    0% {box-shadow: 0 0 5px rgba(34,197,94,0.2);}
    50% {box-shadow: 0 0 20px rgba(34,197,94,0.4);}
    100% {box-shadow: 0 0 5px rgba(34,197,94,0.2);}
}

.header-box {
    animation: fadeIn 0.8s ease-out, glow 3s infinite ease-in-out;
}

</style>

<div class="header-box" style="
    background: linear-gradient(135deg, #0B1220, #0F2A1D);
    padding: 22px;
    border-radius: 18px;
    display: flex;
    align-items: center;
    gap: 18px;
    border: 1px solid rgba(34,197,94,0.25);
">

    <img src="https://upload.wikimedia.org/wikipedia/commons/6/6e/Saudi_Arabia_location_map.svg"
         width="70"
         style="filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.4));">

    <div>
        <h1 style="
            color:#22C55E;
            margin:0;
            font-size:28px;
            font-weight:800;
        ">
            Saudi Arabia Job Market Dashboard
        </h1>

        <p style="
            color:#A7F3D0;
            margin:5px 0 0;
            font-size:14px;
        ">
            📊 Vision 2030 • Job Analytics • AI Insights • Jadarat Dataset
        </p>
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

job_search = st.sidebar.text_input("🔍 Search Job Title")

if job_search:
    df = df[
        df["job_title"]
        .str.contains(job_search, case=False, na=False)
    ]

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

if "city" in df.columns and len(df["city"].dropna()) > 0:

    city_counts = df["city"].value_counts()
    top_city = city_counts.idxmax()
    top_city_count = city_counts.max()

else:
    top_city = "N/A"
    top_city_count = 0


if "job_title" in df.columns and len(df["job_title"].dropna()) > 0:

    job_counts = df["job_title"].value_counts()
    top_job = job_counts.idxmax()
    top_job_count = job_counts.max()

else:
    top_job = "N/A"
    top_job_count = 0


avg_salary = df["Salary"].mean() if "Salary" in df.columns else 0


col1, col2, col3 = st.columns(3)

col1.success(
    f"📍 Top City: {top_city} ({top_city_count:,})"
)

col2.info(
    f"💼 Top Job: {top_job} ({top_job_count:,})"
)

col3.warning(
    f"💰 Avg Salary: {avg_salary:,.0f} SAR" if avg_salary == avg_salary else "💰 Avg Salary: N/A"
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
st.caption(f"Showing {len(df):,} job postings")
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
