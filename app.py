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
# COLOR PALETTE
# =========================
BG_PAGE      = "#F4F6F8"
BG_CARD      = "#FFFFFF"
BORDER       = "#E4E8EC"
TEXT_DARK    = "#1A2B32"
TEXT_MUTED   = "#5C6B73"

GRAD_START   = "#0B4F4A"   # deep teal-green
GRAD_END     = "#1F9D7C"   # emerald
ACCENT_1     = "#0F766E"   # teal
ACCENT_2     = "#B08D57"   # muted gold (contrast accent, used sparingly)
ACCENT_3     = "#2F855A"   # forest green

GREEN_SCALE  = ["#0B4F4A", "#0F766E", "#1F9D7C", "#4FBF9F", "#9AD9C4", "#134E4A"]

FONT_STACK = "'Segoe UI','Helvetica Neue',Arial,sans-serif"

# =========================
# GLOBAL STYLE
# =========================
st.markdown(f"""
<style>
html, body, [class*="css"], [data-testid="stMarkdownContainer"] p {{
font-family: {FONT_STACK} !important;
-webkit-font-smoothing: antialiased;
}}

[data-testid="stAppViewContainer"] {{
background: {BG_PAGE};
}}

h1, h2, h3 {{
color: {TEXT_DARK};
font-weight: 700;
letter-spacing: -0.3px;
}}

p, span, label {{
color: {TEXT_DARK};
font-size: 15px;
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

hr {{
border-color: {BORDER};
}}

div[data-testid="stAlert"] {{
border-radius: 10px;
font-size: 14px;
}}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER (gradient banner with decorative shapes)
# =========================
header_html = (
    f'<div style="position:relative; overflow:hidden; background:linear-gradient(120deg,{GRAD_START},{GRAD_END}); '
    f'padding:32px 30px; border-radius:18px; display:flex; align-items:center; gap:18px;">'
    f'<div style="position:absolute; top:-40px; right:-40px; width:160px; height:160px; border-radius:50%; background:rgba(255,255,255,0.08);"></div>'
    f'<div style="position:absolute; bottom:-60px; right:60px; width:120px; height:120px; border-radius:50%; background:rgba(255,255,255,0.06);"></div>'
    f'<img src="https://upload.wikimedia.org/wikipedia/commons/0/0d/Flag_of_Saudi_Arabia.svg" width="58" '
    f'style="border-radius:6px; box-shadow:0 4px 14px rgba(0,0,0,0.25); position:relative; z-index:1;">'
    f'<div style="position:relative; z-index:1;">'
    f'<h1 style="color:#FFFFFF; margin:0; font-size:28px; font-weight:800;">Saudi Arabia Job Market Dashboard</h1>'
    f'<p style="color:rgba(255,255,255,0.85); margin:4px 0 0 0; font-size:14px; letter-spacing:0.5px;">'
    f'VISION 2030 &nbsp;&bull;&nbsp; JADARAT DATASET</p>'
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
# KPI CARD (accent stripe + icon badge, flat left-aligned HTML)
# =========================
def kpi_card(title, value, icon, accent):
    html = (
        f'<div style="background:{BG_CARD}; border:1px solid {BORDER}; border-radius:14px; '
        f'padding:0; overflow:hidden;">'
        f'<div style="height:5px; background:{accent};"></div>'
        f'<div style="padding:18px; display:flex; align-items:center; gap:14px;">'
        f'<div style="width:44px; height:44px; border-radius:12px; background:{accent}22; '
        f'display:flex; align-items:center; justify-content:center; font-size:22px;">{icon}</div>'
        f'<div>'
        f'<div style="color:{TEXT_MUTED}; font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;">{title}</div>'
        f'<div style="color:{TEXT_DARK}; font-size:24px; font-weight:800;">{value}</div>'
        f'</div></div></div>'
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
    kpi_card("Total Jobs", f"{total_jobs:,}", "📊", ACCENT_1)
with c2:
    kpi_card("Companies", f"{comp:,}", "🏢", ACCENT_3)
with c3:
    kpi_card("Tech Jobs", f"{int(tech_jobs):,}", "💻", ACCENT_2)

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
        font_family=FONT_STACK,
        margin=dict(t=30, b=10, l=10, r=10),
    )
    return fig

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Jobs")
    top_jobs = df["job_title"].value_counts().head(10).reset_index()
    top_jobs.columns = ["job", "count"]
    fig = px.bar(top_jobs, x="count", y="job", orientation="h", text="count")
    fig.update_traces(marker_color=ACCENT_1)
    st.plotly_chart(style_fig(fig), use_container_width=True)

with col2:
    st.subheader("Top Cities")
    top_cities = df["city"].value_counts().head(10).reset_index()
    top_cities.columns = ["city", "count"]
    fig = px.bar(top_cities, x="count", y="city", orientation="h", text="count")
    fig.update_traces(marker_color=ACCENT_3)
    st.plotly_chart(style_fig(fig), use_container_width=True)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Contract Type")
    contract = df["contract"].value_counts().reset_index()
    contract.columns = ["type", "count"]
    fig = px.pie(contract, names="type", values="count", hole=0.55,
                 color_discrete_sequence=GREEN_SCALE)
    st.plotly_chart(style_fig(fig), use_container_width=True)

with col2:
    st.subheader("Salary Distribution")
    fig = px.histogram(df, x="Salary", nbins=25)
    fig.update_traces(marker_color=ACCENT_1)
    st.plotly_chart(style_fig(fig), use_container_width=True)

st.divider()

st.subheader("Tech vs Non-Tech")
tech = df.groupby("is_tech_job")["Salary"].mean().reset_index()
tech["type"] = tech["is_tech_job"].map({0: "Non-Tech", 1: "Tech"})
fig = px.bar(tech, x="type", y="Salary", text="Salary")
fig.update_traces(marker_color=[ACCENT_2, ACCENT_1])
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
