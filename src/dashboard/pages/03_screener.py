import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import (
    get_base_data,
    get_filter_options
)

# ==========================================================
# Page Title
# ==========================================================

st.title("🔍 Stock Screener")

st.write(
    """
    Filter Nifty100 companies using financial and valuation metrics.
    """
)

st.divider()

# ==========================================================
# Load Data
# ==========================================================

df = get_base_data()

filters = get_filter_options()

# ==========================================================
# Sidebar Filters
# ==========================================================

st.sidebar.title("🔍 Screener")

selected_sector = st.sidebar.selectbox(
    "Sector",
    ["All"] + filters["sectors"]
)

selected_market_cap = st.sidebar.selectbox(
    "Market Cap Category",
    ["All"] + sorted(df["market_cap_category"].dropna().unique())
)

min_roe = st.sidebar.slider(
    "Minimum ROE (%)",
    0,
    50,
    15
)

max_pe = st.sidebar.slider(
    "Maximum P/E",
    0,
    100,
    30
)

max_debt = st.sidebar.slider(
    "Maximum Debt to Equity",
    0.0,
    5.0,
    1.0
)

min_quality = st.sidebar.slider(
    "Minimum Quality Score",
    0,
    100,
    60
)# ==========================================================
# Apply Filters
# ==========================================================

filtered_df = df.copy()

if selected_sector != "All":
    filtered_df = filtered_df[
        filtered_df["broad_sector"] == selected_sector
    ]

if selected_market_cap != "All":
    filtered_df = filtered_df[
        filtered_df["market_cap_category"] == selected_market_cap
    ]

filtered_df = filtered_df[
    filtered_df["return_on_equity_pct"] >= min_roe
]

filtered_df = filtered_df[
    filtered_df["pe_ratio"] <= max_pe
]

filtered_df = filtered_df[
    filtered_df["debt_to_equity"] <= max_debt
]

filtered_df = filtered_df[
    filtered_df["composite_quality_score"] >= min_quality
]
# ==========================================================
# Results Summary
# ==========================================================

st.subheader("📊 Screener Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Companies", len(filtered_df))

with col2:
    st.metric(
        "Average ROE",
        f"{filtered_df['return_on_equity_pct'].mean():.2f}%"
    )

with col3:
    st.metric(
        "Average P/E",
        f"{filtered_df['pe_ratio'].mean():.2f}"
    )

with col4:
    st.metric(
        "Average Quality",
        f"{filtered_df['composite_quality_score'].mean():.1f}"
    )

st.divider()

st.subheader("📋 Matching Companies")

columns = [
    "company_id",
    "year",
    "broad_sector",
    "market_cap_crore",
    "pe_ratio",
    "return_on_equity_pct",
    "debt_to_equity",
    "composite_quality_score"
]

st.dataframe(
    filtered_df[columns],
    use_container_width=True,
    hide_index=True,
    height=450
)

st.subheader("📈 ROE vs P/E")

fig = px.scatter(
    filtered_df,
    x="pe_ratio",
    y="return_on_equity_pct",
    color="broad_sector",
    hover_name="company_id",
    size="market_cap_crore"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.download_button(
    label="⬇ Download Results",
    data=filtered_df.to_csv(index=False),
    file_name="stock_screener_results.csv",
    mime="text/csv"
)

st.caption(
    "Filter companies based on financial performance and valuation metrics."
)