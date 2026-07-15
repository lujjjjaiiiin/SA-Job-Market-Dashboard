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
# COLOR PALETTE (professional, muted, eye-friendly)
# =========================
BG_PAGE      = "#F5F6F8"   # light grey page background
BG_CARD      = "#FFFFFF"   # white cards
BORDER       = "#E2E8F0"   # soft grey border
TEXT_DARK    = "#1E293B"   # dark slate for body/headings
TEXT_MUTED   = "#64748B"   # muted grey-blue for labels
GREEN_MAIN   = "#0F766E"   # muted teal-green (headings/accent)
GREEN_SOFT   = "#0D9488"   # slightly lighter accent
GREEN_SCALE  = ["#0F766E", "#14B8A6", "#5EEAD4", "#99F6E4", "#0D9488", "#134E4A"]

# =========================
# GLOBAL STYLE
# =========================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
font-family: 'Inter', 'Segoe UI', sans-serif;
}}

[data-testid="stAppViewContainer"] {{
background: {BG_PAGE};
}}

h1, h2, h3 {{
color: {GREEN_MAIN};
font-weight: 700;
}}

p, span, label, div {{
color: {TEXT_DARK};
}}

[data-testid="stSidebar"] {{
background: {BG_CARD};
border-right: 1px solid {BORDER};
}}

[data-testid="stSidebar"] * {{
color: {TEXT_DARK} !important;
}}

[data-testid="stMetric"] {{
background: {BG_CARD};
border: 1px solid {BORDER};
border-radius: 12px;
padding: 14px;
}}

[data-testid="stMetricValue"] {{
color: {GREEN_MAIN};
}}

hr {{
border-color: {BORDER};
}}

div[data-testid="stAlert"] {{
border-radius: 10px;
}}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
header_html = (
    f'<div style="background:{BG_CARD}; padding:22px; border-radius:14px; '
    f'display:flex; align-items:center; gap:15px; border:1px solid {BORDER};">'
    f'<img src="https://upload.wikimedia.org/wikipedia/commons/0/0d/Flag_of_Saudi_Arabia.svg" width="55">'
    f'<div>'
    f'<h1 style="color:{GREEN_MAIN}; margin:0; font-size:26px;">Saudi Arabia Job Market Dashboard</h1>'
    f'<p style="color:{TEXT_MUTED}; margin:0; font-size:14px;">Vision 2030 &bull; Jadarat Dataset</p>'
    f'</div></div>'
)
st.markdown(header_html, unsafe_allow_html=True)
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
# KPI CARD (no leading indentation -> avoids markdown code-block bug)
# =========================
def kpi_card(title, value, icon):
    html = (
        f'<div style="background:{BG_CARD}; border:1px solid {BORDER}; padding:18px; '
        f'border-radius:14px; text-align:center;">'
        f'<div style="font-size:26px;">{icon}</div>'
        f'<h2 style="color:{GREEN_MAIN}; margin:6px 0; font-size:22px;">{value}</h2>'
        f'<p style="color:{TEXT_MUTED}; margin:0; font-size:13px;">{title}</p>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

# =========================
# KPI ROW
# =========================
df["is_tech_job"] = pd.to_numeric(df["is_tech_job"], errors="coerce").fillna(0)

total_jobs = len(df)
tech_jobs = df["is_tech_job"].sum()
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
def style_fig(fig):
    fig.update_layout(
        template="plotly_white",
        plot_bgcolor=BG_CARD,
        paper_bgcolor=BG_CARD,
        font_color=TEXT_DARK,
        margin=dict(t=30, b=10, l=10, r=10),
    )
    return fig

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Jobs")
    top_jobs = df["job_title"].value_counts().head(10).reset_index()
    top_jobs.columns = ["job", "count"]
    fig = px.bar(top_jobs, x="count", y="job", orientation="h", text="count")
    fig.update_traces(marker_color=GREEN_MAIN)
    st.plotly_chart(style_fig(fig), use_container_width=True)

with col2:
    st.subheader("Top Cities")
    top_cities = df["city"].value_counts().head(10).reset_index()
    top_cities.columns = ["city", "count"]
    fig = px.bar(top_cities, x="count", y="city", orientation="h", text="count")
    fig.update_traces(marker_color=GREEN_SOFT)
    st.plotly_chart(style_fig(fig), use_container_width=True)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Contract Type")
    contract = df["contract"].value_counts().reset_index()
    contract.columns = ["type", "count"]
    fig = px.pie(contract, names="type", values="count", hole=0.5,
                 color_discrete_sequence=GREEN_SCALE)
    st.plotly_chart(style_fig(fig), use_container_width=True)

with col2:
    st.subheader("Salary Distribution")
    fig = px.histogram(df, x="Salary", nbins=25)
    fig.update_traces(marker_color=GREEN_SOFT)
    st.plotly_chart(style_fig(fig), use_container_width=True)

st.divider()

st.subheader("Tech vs Non-Tech")
tech = df.groupby("is_tech_job")["Salary"].mean().reset_index()
tech["type"] = tech["is_tech_job"].map({0: "Non-Tech", 1: "Tech"})
fig = px.bar(tech, x="type", y="Salary", text="Salary")
fig.update_traces(marker_color=[TEXT_MUTED, GREEN_MAIN])
st.plotly_chart(style_fig(fig), use_container_width=True)

st.divider()

st.subheader("📋 Raw Data")
st.dataframe(df, use_container_width=True)

st.download_button(
    "📥 Download Data",
    df.to_csv(index=False),
    "jadarat.csv",
    "text/csv"
)
