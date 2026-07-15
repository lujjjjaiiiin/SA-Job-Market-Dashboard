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

GRAD_START   = "#0B4F4A"
GRAD_END     = "#1F9D7C"
ACCENT_1     = "#0F766E"
ACCENT_2     = "#B08D57"
ACCENT_3     = "#2F855A"

GREEN_SCALE  = ["#0B4F4A", "#0F766E", "#1F9D7C", "#4FBF9F", "#9AD9C4", "#134E4A"]

FONT_STACK = "'Segoe UI','Helvetica Neue',Arial,sans-serif"

# =========================
# GLOBAL STYLE
# =========================
st.markdown(f"""
<style>
html, body {{
font-family: {FONT_STACK};
-webkit-font-smoothing: antialiased;
}}

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMetricLabel"],
[data-testid="stMetricValue"] {{
font-family: {FONT_STACK};
}}

[data-testid="stAppViewContainer"] {{
background: #FAFBFA;
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

/* ---- Sidebar redesign ---- */
[data-testid="stSidebar"] {{
background-color: #EAF7F1;
background-image: url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20width%3D%22400%22%20height%3D%22180%22%20viewBox%3D%220%200%20400%20180%22%3E%3Cpath%20d%3D%22M0%2040%20C%20100%2090%2C%20300%200%2C%20400%2050%20L400%200%20L0%200%20Z%22%20fill%3D%22%23DFF3EC%22/%3E%3Cpath%20d%3D%22M0%2090%20C%20120%2040%2C%20280%20140%2C%20400%2090%20L400%20180%20L0%20180%20Z%22%20fill%3D%22%23CDEDE1%22/%3E%3Cpath%20d%3D%22M0%20130%20C%20100%20170%2C%20300%2090%2C%20400%20130%20L400%20180%20L0%20180%20Z%22%20fill%3D%22%23B9E4D3%22/%3E%3C/svg%3E");
background-repeat: repeat-y;
background-size: 100% 220px;
border-right: 2px solid {ACCENT_1};
padding-top: 6px;
}}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] li {{
color: {TEXT_DARK};
font-size: 14px;
}}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {{
font-size: 16px !important;
font-weight: 800 !important;
color: {ACCENT_1} !important;
}}

[data-testid="stSidebar"] label p {{
font-size: 13px !important;
font-weight: 700 !important;
color: {TEXT_DARK} !important;
text-transform: uppercase;
letter-spacing: 0.4px;
margin-bottom: 4px !important;
}}

/* Boxed dropdowns (multiselect) */
[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
background: #FFFFFF !important;
border: 1.5px solid {BORDER} !important;
border-radius: 10px !important;
box-shadow: 0 2px 6px rgba(15,23,42,0.05);
min-height: 42px;
}}

[data-testid="stSidebar"] div[data-baseweb="select"]:focus-within > div {{
border: 1.5px solid {ACCENT_1} !important;
}}

/* Boxed text input */
[data-testid="stSidebar"] input[type="text"] {{
background: #FFFFFF !important;
border: 1.5px solid {BORDER} !important;
border-radius: 10px !important;
padding: 10px 12px !important;
box-shadow: 0 2px 6px rgba(15,23,42,0.05);
}}

[data-testid="stSidebar"] input[type="text"]:focus {{
border: 1.5px solid {ACCENT_1} !important;
outline: none !important;
}}

/* Boxed radio group */
[data-testid="stSidebar"] [role="radiogroup"] {{
background: #FFFFFF;
border: 1.5px solid {BORDER};
border-radius: 10px;
padding: 12px 14px;
box-shadow: 0 2px 6px rgba(15,23,42,0.05);
}}

[data-testid="stSidebar"] [data-baseweb="radio"] label {{
font-size: 13.5px !important;
font-weight: 500 !important;
}}

/* Section spacing between widgets */
[data-testid="stSidebar"] .stMultiSelect,
[data-testid="stSidebar"] .stRadio,
[data-testid="stSidebar"] .stTextInput {{
margin-bottom: 14px;
}}

/* ---- KPI cards shadow ---- */
[data-testid="stMetric"] {{
background: {BG_CARD};
border: 1px solid {BORDER};
border-radius: 12px;
padding: 14px;
box-shadow: 0 6px 16px rgba(15,23,42,0.06);
}}

hr {{
border-color: {BORDER};
}}

div[data-testid="stAlert"] {{
border-radius: 10px;
font-size: 14px;
box-shadow: 0 4px 12px rgba(15,23,42,0.05);
}}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER (gradient banner with decorative shapes)
# =========================
header_html = (
    f'<div style="position:relative; overflow:hidden; background:linear-gradient(120deg,{GRAD_START},{GRAD_END}); '
    f'padding:32px 30px; border-radius:18px; display:flex; align-items:center; gap:18px; '
    f'box-shadow:0 14px 30px rgba(11,79,74,0.25);">'
    f'<div style="position:absolute; top:-40px; right:-40px; width:160px; height:160px; border-radius:50%; background:rgba(255,255,255,0.08);"></div>'
    f'<div style="position:absolute; bottom:-60px; right:60px; width:120px; height:120px; border-radius:50%; background:rgba(255,255,255,0.06);"></div>'
    f'<img src="https://upload.wikimedia.org/wikipedia/commons/0/0d/Flag_of_Saudi_Arabia.svg" width="58" '
    f'style="border-radius:6px; box-shadow:0 4px 14px rgba(0,0,0,0.25); position:relative; z-index:1;">'
    f'<div style="position:relative; z-index:1;">'
    f'<h1 style="color:#FFFFFF; margin:0; font-size:58px; font-weight:800; line-height:1.15;">Saudi Arabia Job Market Dashboard</h1>'
    f'<p style="color:rgba(255,255,255,0.85); margin:4px 0 0 0; font-size:14px; letter-spacing:0.5px;">'
    f'VISION 2030 &nbsp;&bull;&nbsp; JADARAT DATASET</p>'
    f'</div></div>'
)
st.markdown(header_html, unsafe_allow_html=True)
st.write("")

# =========================
# SIDEBAR FILTERS
# =========================
sidebar_title_html = (
    f'<div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">'
    f'<div style="width:6px; height:18px; background:{ACCENT_1}; border-radius:3px;"></div>'
    f'<span style="font-size:15px; font-weight:700; color:{TEXT_DARK};">Filters</span></div>'
)
st.sidebar.markdown(sidebar_title_html, unsafe_allow_html=True)

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

job_search = st.sidebar.text_input("Search Job Title")

if job_search:
    df = df[df["job_title"].str.contains(job_search, case=False, na=False)]

if df.empty:
    st.warning("No data after filters")
    st.stop()

# =========================
# KPI CARD (shadow + accent stripe + icon badge)
# =========================
def kpi_card(title, value, icon, accent):
    html = (
        f'<div style="background:{BG_CARD}; border:1px solid {BORDER}; border-radius:14px; '
        f'overflow:hidden; box-shadow:0 10px 24px rgba(15,23,42,0.08); transition:all 0.2s ease;">'
        f'<div style="height:5px; background:{accent};"></div>'
        f'<div style="padding:18px; display:flex; align-items:center; gap:14px;">'
        f'<div style="width:44px; height:44px; border-radius:12px; background:{accent}22; '
        f'display:flex; align-items:center; justify-content:center; font-size:22px; '
        f'box-shadow: inset 0 0 0 1px {accent}33;">{icon}</div>'
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
# CHARTS (explicit text/axis colors so nothing renders white-on-white)
# =========================
def style_fig(fig):
    fig.update_layout(
        template="plotly_white",
        plot_bgcolor=BG_CARD,
        paper_bgcolor=BG_CARD,
        font=dict(color=TEXT_DARK, family=FONT_STACK, size=13),
        title_font=dict(color=TEXT_DARK),
        legend=dict(font=dict(color=TEXT_DARK)),
        xaxis=dict(color=TEXT_DARK, title_font=dict(color=TEXT_DARK), tickfont=dict(color=TEXT_DARK), gridcolor=BORDER),
        yaxis=dict(color=TEXT_DARK, title_font=dict(color=TEXT_DARK), tickfont=dict(color=TEXT_DARK), gridcolor=BORDER),
        margin=dict(t=30, b=10, l=10, r=10),
    )
    fig.update_traces(selector=dict(type="bar"), textfont=dict(color=TEXT_DARK), textposition="outside")
    fig.update_traces(selector=dict(type="pie"), textfont=dict(color=TEXT_DARK))
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
    fig.update_traces(textfont=dict(color="#FFFFFF"))
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
