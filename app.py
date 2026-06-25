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
# HEADER (CLEAN + MODERN)
# =========================
st.markdown("""
<div style="
    background: linear-gradient(135deg,#0B1220,#0F2A1D);
    padding:20px;
    border-radius:16px;
    border:1px solid rgba(34,197,94,0.3);
">
<h1 style="color:#22C55E;margin:0;">🇸🇦 Saudi Job Market Dashboard</h1>
<p style="color:#A7F3D0;margin:5px 0 0;">Vision 2030 • Jadarat Dataset • Analytics</p>
</div>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
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

job_search = st.sidebar.text_input("🔍 Search Job Title")

if job_search:
    df = df[df["job_title"].str.contains(job_search, case=False, na=False)]

if df.empty:
    st.warning("No data after filters")
    st.stop()

# =========================
# SAFE KPI FORMAT
# =========================
def fmt(x):
    if x >= 1_000_000:
        return f"{x/1_000_000:.1f}M"
    if x >= 1_000:
        return f"{x/1_000:.1f}K"
    return str(int(x))

# =========================
# KPI ROW
# =========================
c1, c2, c3, c4 = st.columns(4)

c1.metric("📌 Jobs", fmt(len(df)))
c2.metric("🏢 Companies", fmt(df["comp_name"].nunique()) if "comp_name" in df else "N/A")
c3.metric("💻 Tech Jobs", fmt(df["is_tech_job"].sum()))
c3.metric("📊 Tech %", f"{df['is_tech_job'].mean()*100:.1f}%")

st.divider()

# =========================
# INSIGHTS (SAFE)
# =========================
st.subheader("📈 Key Insights")

top_city = df["city"].value_counts().idxmax() if "city" in df else "N/A"
top_job = df["job_title"].value_counts().idxmax()
avg_salary = df["Salary"].mean() if "Salary" in df else 0

a, b, c = st.columns(3)

a.success(f"📍 Top City: {top_city}")
b.info(f"💼 Top Job: {top_job}")
c.warning(f"💰 Avg Salary: {avg_salary:,.0f} SAR")

st.divider()

# =========================
# TOP JOBS & CITIES (PLOTLY)
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Jobs")
    top_jobs = df["job_title"].value_counts().head(10).reset_index()
    top_jobs.columns = ["job", "count"]

    fig = px.bar(top_jobs, x="count", y="job", orientation="h", text="count")
    fig.update_layout(template="plotly_dark")
    fig.update_traces(marker_color="#22C55E")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Top Cities")
    top_cities = df["city"].value_counts().head(10).reset_index()
    top_cities.columns = ["city", "count"]

    fig = px.bar(top_cities, x="count", y="city", orientation="h", text="count")
    fig.update_layout(template="plotly_dark")
    fig.update_traces(marker_color="#16A34A")
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# =========================
# CONTRACT + SALARY
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Contract Type")

    contract = df["contract"].value_counts().reset_index()
    contract.columns = ["type", "count"]

    fig = px.pie(contract, names="type", values="count", hole=0.5)
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Salary Distribution")

    fig = px.histogram(df, x="Salary", nbins=25)
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# =========================
# TECH ANALYSIS
# =========================
st.subheader("Tech vs Non-Tech")

tech = df.groupby("is_tech_job")["Salary"].mean().reset_index()
tech["type"] = tech["is_tech_job"].map({0: "Non-Tech", 1: "Tech"})

fig = px.bar(tech, x="type", y="Salary", text="Salary")
fig.update_layout(template="plotly_dark")
fig.update_traces(marker_color=["#EF4444", "#22C55E"])

st.plotly_chart(fig, use_container_width=True)

# =========================
# DATA
# =========================
st.caption(f"Rows: {len(df):,}")
st.dataframe(df, use_container_width=True)

# =========================
# DOWNLOAD
# =========================
st.download_button(
    "📥 Download Data",
    df.to_csv(index=False),
    "jadarat.csv",
    "text/csv"
)
