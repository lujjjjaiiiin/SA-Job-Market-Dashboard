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

TECH_PATTERN = r'\bdata scientist\b|\bdata analyst\b|\bsoftware\b|\bdeveloper\b|\bai\b|\bmachine learning\b|\bpython\b|\bjava\b|\bsql\b|\banalyst\b'

df["is_tech_job"] = (
    df["job_title"]
    .str.lower()
    .str.contains(TECH_PATTERN, na=False)
    .astype(int)
)

# =========================
# STYLE (GREEN & WHITE THEME)
# =========================
st.markdown("""
<style>

.main {
    background: linear-gradient(180deg,#F8FAFC,#F1F5F9);
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg,#F8FAFC,#F1F5F9);
}

h1, h2, h3 {
    color: #15803D;
    font-family: 'Segoe UI', sans-serif;
}

p, span, label, div {
    font-family: 'Segoe UI', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#FFFFFF,#DCFCE7);
    border-right: 2px solid #22C55E;
}

[data-testid="stSidebar"] * {
    color: #14532D !important;
}

/* Metric widgets */
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #BBF7D0;
    border-radius: 14px;
    padding: 12px;
    box-shadow: 0 4px 14px rgba(34,197,94,0.10);
}

[data-testid="stMetricValue"] {
    color: #15803D;
}

/* Divider */
hr {
    border-color: #BBF7D0;
}

/* Success/info/warning boxes */
div[data-testid="stAlert"] {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("""
<div style="
    background: linear-gradient(135deg,#FFFFFF,#DCFCE7);
    padding:25px;
    border-radius:18px;
    display:flex;
    align-items:center;
    gap:15px;
    border: 1px solid #BBF7D0;
    box-shadow: 0 8px 24px rgba(34,197,94,0.12);
">

<img src="https://upload.wikimedia.org/wikipedia/commons/0/0d/Flag_of_Saudi_Arabia.svg" width="60">

<div>
<h1 style="color:#15803D;margin:0;">Saudi Arabia Job Market Dashboard</h1>
<p style="color:#16A34A;margin:0;">🇸🇦 Vision 2030 • Jadarat Dataset</p>
</div>

</div>
""", unsafe_allow_html=True)

st.write("")

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

job_search = st.sidebar.text_input("🔎 Search Job Title")

if job_search:
    df = df[df["job_title"].str.contains(job_search, case=False, na=False)]

if df.empty:
    st.warning("No data after filters")
    st.stop()

# =========================
# FORMAT NUMBERS
# =========================
def fmt(x):
    try:
        x = float(x)
    except:
        return "0"

    if x >= 1_000_000:
        return f"{x/1_000_000:.1f}M"
    if x >= 1_000:
        return f"{x/1_000:.1f}K"
    return str(int(x))

# =========================
# KPI CARD (GREEN & WHITE)
# =========================
def kpi_card(title, value, icon, color="#15803D"):
    st.markdown(f"""
    <div style="
        background: #FFFFFF;
        border: 1px solid #BBF7D0;
        padding: 18px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0 8px 22px rgba(34,197,94,0.10);
        transition: all 0.3s ease-in-out;
    "
    onmouseover="this.style.transform='scale(1.05)';this.style.boxShadow='0 12px 28px rgba(34,197,94,0.18)';"
    onmouseout="this.style.transform='scale(1)';this.style.boxShadow='0 8px 22px rgba(34,197,94,0.10)';">

        <div style="font-size:30px;">{icon}</div>

        <h2 style="color:{color}; margin:8px 0; font-size:22px;">
            {value}
        </h2>

        <p style="color:#16A34A; margin:0; font-size:13px;">
            {title}
        </p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# KPI ROW
# =========================
df["is_tech_job"] = pd.to_numeric(df["is_tech_job"], errors="coerce").fillna(0)

total_jobs = len(df)
tech_jobs = df["is_tech_job"].sum()
tech_pct = (tech_jobs / total_jobs * 100) if total_jobs > 0 else 0
comp = df["comp_name"].nunique() if "comp_name" in df.columns else 0

c1, c2, c3 = st.columns(3)

with c1:
    kpi_card("Total Jobs", f"{total_jobs:,}", "📊")
with c2:
    kpi_card("Companies", f"{comp:,}", "🏢")
with c3:
    kpi_card("Tech Jobs", f"{int(tech_jobs):,}", "💻")

st.divider()

# =========================
# INSIGHTS
# =========================
top_city = df["city"].value_counts().idxmax() if "city" in df else "N/A"
top_job = df["job_title"].value_counts().idxmax()

avg_salary = df["Salary"].mean() if "Salary" in df else 0

a, b, c = st.columns(3)

a.success(f"📍 Top City: {top_city}")
b.info(f"💼 Top Job: {top_job}")
c.warning(f"💰 Avg Salary: {avg_salary:,.0f} SAR")

st.divider()

# =========================
# CHARTS
# =========================
GREEN_SCALE = ["#BBF7D0", "#86EFAC", "#4ADE80", "#22C55E", "#16A34A", "#15803D"]

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Jobs")
    top_jobs = df["job_title"].value_counts().head(10).reset_index()
    top_jobs.columns = ["job", "count"]

    fig = px.bar(top_jobs, x="count", y="job", orientation="h", text="count")
    fig.update_layout(
        template="plotly_white",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_color="#14532D",
    )
    fig.update_traces(marker_color="#22C55E")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Top Cities")
    top_cities = df["city"].value_counts().head(10).reset_index()
    top_cities.columns = ["city", "count"]

    fig = px.bar(top_cities, x="count", y="city", orientation="h", text="count")
    fig.update_layout(
        template="plotly_white",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_color="#14532D",
    )
    fig.update_traces(marker_color="#15803D")
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

    fig = px.pie(
        contract, names="type", values="count", hole=0.5,
        color_discrete_sequence=GREEN_SCALE
    )
    fig.update_layout(
        template="plotly_white",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_color="#14532D",
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Salary Distribution")

    fig = px.histogram(df, x="Salary", nbins=25)
    fig.update_layout(
        template="plotly_white",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_color="#14532D",
    )
    fig.update_traces(marker_color="#4ADE80")
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# =========================
# TECH
# =========================
st.subheader("Tech vs Non-Tech")

tech = df.groupby("is_tech_job")["Salary"].mean().reset_index()
tech["type"] = tech["is_tech_job"].map({0: "Non-Tech", 1: "Tech"})

fig = px.bar(tech, x="type", y="Salary", text="Salary")
fig.update_layout(
    template="plotly_white",
    plot_bgcolor="white",
    paper_bgcolor="white",
    font_color="#14532D",
)
fig.update_traces(marker_color=["#94A3B8", "#22C55E"])

st.plotly_chart(fig, use_container_width=True)

st.divider()

# =========================
# DATA
# =========================
st.subheader("📋 Raw Data")
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
