import streamlit as st
import plotly.express as px

from utils.db import (
    get_company_list,
    get_company_profile
)
# ==========================================================
# Page Title
# ==========================================================

st.title("🏢 Company Profile")

st.write(
    """
    Explore detailed financial information for any
    Nifty100 company.
    """
)

st.divider()

# ==========================================================
# Load Company List
# ==========================================================

companies = get_company_list()

# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.title("🏢 Company Profile")

selected_company = st.sidebar.selectbox(
    "Select Company",
    companies
)

# ==========================================================
# Company Data
# ==========================================================

company_data = get_company_profile(selected_company)

st.dataframe(company_data)
# ==========================================================
# Company Overview
# ==========================================================

latest = company_data.sort_values("year").iloc[-1]

st.subheader(f"🏢 {selected_company}")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Market Cap (₹ Cr)",
        f"{latest['market_cap_crore']:,.0f}"
    )

with col2:
    st.metric(
        "P/E Ratio",
        f"{latest['pe_ratio']:.2f}"
    )

with col3:
    st.metric(
        "ROE",
        f"{latest['return_on_equity_pct']:.2f}%"
    )

with col4:
    st.metric(
        "Quality Score",
        f"{latest['composite_quality_score']:.1f}"
    )

st.divider()

st.subheader("Financial History")

st.dataframe(
    company_data,
    use_container_width=True,
    hide_index=True
)
# ==========================================================
# Company Information
# ==========================================================

st.subheader("📋 Company Information")

info_col1, info_col2 = st.columns(2)

with info_col1:
    st.write("**Sector:**", latest["broad_sector"])
    st.write("**Sub Sector:**", latest["sub_sector"])

with info_col2:
    st.write("**Market Cap Category:**", latest["market_cap_category"])
    st.write("**Index Weight:**", f"{latest['index_weight_pct']:.2f}%")

st.divider()

st.subheader("📈 Return on Equity Trend")

fig = px.line(
    company_data,
    x="year",
    y="return_on_equity_pct",
    markers=True,
    title="Return on Equity"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("💰 Earnings Per Share")

fig = px.line(
    company_data,
    x="year",
    y="earnings_per_share",
    markers=True,
    title="EPS"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("📊 Financial History")

st.dataframe(
    company_data,
    use_container_width=True,
    hide_index=True,
    height=450
)