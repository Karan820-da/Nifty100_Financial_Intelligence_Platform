import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import get_engine

st.title("💰 Valuation Analysis")

st.write(
    "Analyze valuation metrics, compare companies with their sector, and identify overvalued or undervalued stocks."
)

st.divider()

engine = get_engine()

query = """
SELECT
    fr.company_id,
    c.company_name,
    fr.year,
    s.broad_sector,
    s.sub_sector,

    mc.market_cap_crore,
    mc.pe_ratio,
    mc.pb_ratio,
    mc.ev_ebitda,

    fr.free_cash_flow_cr

FROM financial_ratios fr

LEFT JOIN companies c
    ON fr.company_id = c.id

LEFT JOIN sectors s
    ON fr.company_id = s.company_id

LEFT JOIN market_cap mc
    ON fr.company_id = mc.company_id
   AND RIGHT(fr.year,4)=CAST(mc.year AS CHAR)

WHERE c.company_name IS NOT NULL;
"""

df = pd.read_sql(query, engine)

# -----------------------------
# Numeric Conversion
# -----------------------------

numeric_cols = [
    "market_cap_crore",
    "pe_ratio",
    "pb_ratio",
    "ev_ebitda",
    "free_cash_flow_cr"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# -----------------------------
# Calculations
# -----------------------------

df["fcf_yield_pct"] = (
    df["free_cash_flow_cr"] /
    df["market_cap_crore"]
) * 100

sector_pe = (
    df.groupby("broad_sector")["pe_ratio"]
      .median()
      .rename("sector_median_pe")
)

df = df.merge(
    sector_pe,
    on="broad_sector",
    how="left"
)

df["pe_vs_sector"] = (
    (df["pe_ratio"] - df["sector_median_pe"])
    / df["sector_median_pe"]
) * 100


def valuation_flag(row):

    if pd.isna(row["pe_ratio"]) or pd.isna(row["sector_median_pe"]):
        return "No Data"

    if row["pe_ratio"] > row["sector_median_pe"] * 1.5:
        return "Caution"

    if row["pe_ratio"] < row["sector_median_pe"] * 0.7:
        return "Discount"

    return "Fair"


df["flag"] = df.apply(valuation_flag, axis=1)

# -----------------------------
# Filters
# -----------------------------

st.sidebar.header("Filters")

sector = st.sidebar.selectbox(
    "Sector",
    ["All"] + sorted(df["broad_sector"].dropna().unique().tolist())
)

flag = st.sidebar.selectbox(
    "Valuation Flag",
    ["All", "Fair", "Discount", "Caution", "No Data"]
)

if sector != "All":
    df = df[df["broad_sector"] == sector]

if flag != "All":
    df = df[df["flag"] == flag]

# -----------------------------
# KPIs
# -----------------------------

st.subheader("📊 Valuation Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Companies", df["company_id"].nunique())

with c2:
    st.metric(
        "Average PE",
        round(df["pe_ratio"].mean(skipna=True), 2)
    )

with c3:
    st.metric(
        "Average PB",
        round(df["pb_ratio"].mean(skipna=True), 2)
    )

with c4:
    st.metric(
        "Average FCF Yield %",
        round(df["fcf_yield_pct"].mean(skipna=True), 2)
    )

st.divider()

# -----------------------------
# Charts
# -----------------------------

st.subheader("📈 Valuation Flag Distribution")

flag_chart = px.pie(
    df,
    names="flag",
    title="Valuation Flags"
)

st.plotly_chart(flag_chart, use_container_width=True)

st.subheader("🏭 Sector Median PE")

sector_chart = (
    df.groupby("broad_sector")["sector_median_pe"]
      .first()
      .reset_index()
)

fig = px.bar(
    sector_chart,
    x="broad_sector",
    y="sector_median_pe",
    title="Sector Median PE"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Data Table
# -----------------------------

st.subheader("📋 Valuation Data")

st.dataframe(
    df[
        [
            "company_name",
            "year",
            "broad_sector",
            "pe_ratio",
            "pb_ratio",
            "ev_ebitda",
            "fcf_yield_pct",
            "sector_median_pe",
            "flag"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# Export
# -----------------------------

st.subheader("⬇ Export")

csv = df.to_csv(index=False)

st.download_button(
    "📥 Download Valuation Report (CSV)",
    csv,
    "valuation_report.csv",
    "text/csv"
)

st.divider()

st.caption(
    "Sprint 4 • Valuation Analytics | Nifty100 Financial Intelligence Platform"
)