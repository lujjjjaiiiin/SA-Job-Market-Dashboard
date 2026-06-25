# -*- coding: utf-8 -*-
st.sidebar.header("🔎 Filters")

# -----------------------
# CITY FILTER
# -----------------------
if "city" in df.columns:
    cities = st.sidebar.multiselect(
        "City",
        df["city"].dropna().unique()
    )
    if cities:
        df = df[df["city"].isin(cities)]

# -----------------------
# CONTRACT FILTER
# -----------------------
if "contract" in df.columns:
    contracts = st.sidebar.multiselect(
        "Contract Type",
        df["contract"].dropna().unique()
    )
    if contracts:
        df = df[df["contract"].isin(contracts)]

# -----------------------
# TECH / NON-TECH FILTER ⭐
# -----------------------
tech_filter = st.sidebar.radio(
    "Job Type",
    ["All", "Tech Only", "Non-Tech Only"]
)

if tech_filter == "Tech Only":
    df = df[df["is_tech_job"] == 1]

elif tech_filter == "Non-Tech Only":
    df = df[df["is_tech_job"] == 0]
