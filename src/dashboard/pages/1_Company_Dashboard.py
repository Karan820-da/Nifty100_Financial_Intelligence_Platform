import streamlit as st

from src.reports.data_loader import (
    load_company,
    load_market_cap,
    load_ratios,
)

st.set_page_config(layout="wide")

st.title("📊 Company Dashboard")

company_id = st.sidebar.selectbox(
    "Select Company",
    [
        "TCS",
        "INFY",
        "RELIANCE",
        "HDFCBANK",
        "ICICIBANK"
    ]
)

company = load_company(company_id)
market = load_market_cap(company_id)
ratios = load_ratios(company_id)

latest = ratios.iloc[-1]

st.header(company.iloc[0]["company_name"])

col1, col2, col3 = st.columns(3)

col1.metric(
    "Market Cap",
    f"₹{market.iloc[0]['market_cap_crore']:,.0f} Cr"
)

col2.metric(
    "PE Ratio",
    f"{market.iloc[0]['pe_ratio']:.2f}"
)

col3.metric(
    "ROE",
    f"{company.iloc[0]['roe_percentage']*100:.2f}%"
)

col4, col5, col6 = st.columns(3)

col4.metric(
    "ROCE",
    f"{company.iloc[0]['roce_percentage']:.2f}%"
)

col5.metric(
    "EPS",
    f"₹{latest['earnings_per_share']:.2f}"
)

col6.metric(
    "Dividend",
    f"{latest['dividend_payout_ratio_pct']:.2f}%"
)