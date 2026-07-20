# ==========================================================
# Home Dashboard
# ==========================================================

import streamlit as st
import plotly.express as px

from utils.db import (
    get_home_data,
    get_market_summary,
    get_filter_options,
    get_top_companies
)
# ==========================================================
# Load Dashboard Data
# ==========================================================

home_data = get_home_data()

market_summary = get_market_summary()

filters = get_filter_options()

# ==========================================================
# Sidebar Filters
# ==========================================================

st.sidebar.header("Dashboard Filters")

selected_company = st.sidebar.selectbox(
    "Select Company",
    filters["companies"]
)

selected_year = st.sidebar.selectbox(
    "Select Year",
    filters["years"]
)

selected_sector = st.sidebar.selectbox(
    "Select Sector",
    filters["sectors"]
)

# ==========================================================
# KPI Cards
# ==========================================================

st.markdown("## 📊 Market Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Companies",
        market_summary["total_companies"]
    )

with col2:
    st.metric(
        "Sectors",
        market_summary["total_sectors"]
    )

with col3:
    st.metric(
        "Average P/E",
        market_summary["average_pe"]
    )

with col4:
    st.metric(
        "Average ROE",
        f"{market_summary['average_roe']}%"
    )

with col5:
    st.metric(
        "Market Cap (Cr)",
        f"{market_summary['total_market_cap']:,.0f}"
    )

# ==========================================================
# Top Companies
# ==========================================================

st.markdown("## 🏆 Top 10 Companies by Market Capitalization")

top_companies = get_top_companies("market_cap_crore")

display_columns = [
    "company_id",
    "market_cap_crore",
    "pe_ratio",
    "return_on_equity_pct",
    "composite_quality_score"
]

st.dataframe(
    top_companies[display_columns],
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# Market Capitalization Chart
# ==========================================================

st.markdown("## 📈 Top 10 Companies by Market Capitalization")

fig = px.bar(
    top_companies,
    x="market_cap_crore",
    y="company_id",
    orientation="h",
    title="Top 10 Companies by Market Capitalization",
    labels={
        "company_id": "Company",
        "market_cap_crore": "Market Cap (₹ Crore)"
    }
)

fig.update_layout(
    yaxis=dict(categoryorder="total ascending"),
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)