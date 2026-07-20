import streamlit as st
import pandas as pd

from utils.db import get_base_data

st.title("📄 Reports & Export")

st.write(
    "View dataset statistics, preview the financial data, and export reports."
)

st.divider()

df = get_base_data()

st.subheader("📊 Dataset Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Records", len(df))

with col2:
    st.metric("Companies", df["company_id"].nunique())

with col3:
    st.metric("Sectors", df["broad_sector"].nunique())

with col4:
    st.metric("Years", df["year"].nunique())

st.subheader("📈 Financial Statistics")

stats = df[
    [
        "market_cap_crore",
        "pe_ratio",
        "return_on_equity_pct",
        "debt_to_equity",
        "composite_quality_score"
    ]
].describe()

st.dataframe(
    stats,
    use_container_width=True
)

st.subheader("📋 Dataset Preview")

st.dataframe(
    df.head(20),
    use_container_width=True,
    hide_index=True
)

st.subheader("⬇ Export Data")

csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download Dataset (CSV)",
    data=csv,
    file_name="nifty100_financial_data.csv",
    mime="text/csv"
)

st.subheader("ℹ️ Project Information")

st.info(
    """
### Nifty100 Financial Intelligence Platform

**Features**
- Home Dashboard
- Company Profile
- Stock Screener
- Peer Comparison
- Market Trends
- Sector Analysis
- Market Capitalization Dashboard
- Reports & Export

**Technology Stack**
- Python
- Streamlit
- MySQL
- SQLAlchemy
- Pandas
- Plotly Express

This dashboard helps analyze Nifty100 companies using financial ratios, market capitalization, valuation metrics, and sector-wise insights.
"""
)

st.divider()

st.caption(
    "Developed as a Financial Analytics Capstone Project using Python, Streamlit, MySQL, SQLAlchemy, Pandas, and Plotly."
)