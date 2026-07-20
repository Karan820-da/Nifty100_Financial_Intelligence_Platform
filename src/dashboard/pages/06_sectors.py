import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import (
    get_base_data,
    get_filter_options
)

st.title("🏭 Sector Analysis")

st.write(
    "Analyze financial performance across different market sectors."
)

st.divider()

df = get_base_data()
filters = get_filter_options()

selected_sector = st.selectbox(
    "Select Sector",
    ["All"] + filters["sectors"]
)

sector_df = df.copy()

if selected_sector != "All":
    sector_df = sector_df[
        sector_df["broad_sector"] == selected_sector
    ]

st.subheader("📊 Sector Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Companies", sector_df["company_id"].nunique())

with col2:
    st.metric(
        "Average ROE",
        f"{sector_df['return_on_equity_pct'].mean():.2f}%"
    )

with col3:
    st.metric(
        "Average P/E",
        f"{sector_df['pe_ratio'].mean():.2f}"
    )

with col4:
    st.metric(
        "Total Market Cap",
        f"₹{sector_df['market_cap_crore'].sum():,.0f} Cr"
    )

st.subheader("📈 Sector Comparison")

sector_summary = (
    df.groupby("broad_sector")
      .agg({
          "return_on_equity_pct":"mean",
          "pe_ratio":"mean",
          "market_cap_crore":"sum"
      })
      .reset_index()
)

fig = px.bar(
    sector_summary,
    x="broad_sector",
    y="return_on_equity_pct",
    color="broad_sector",
    title="Average ROE by Sector"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🏆 Top Companies")

top_companies = sector_df.nlargest(
    10,
    "market_cap_crore"
)

fig = px.bar(
    top_companies,
    x="company_id",
    y="market_cap_crore",
    color="company_id"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("📋 Companies")

columns = [
    "company_id",
    "broad_sector",
    "sub_sector",
    "market_cap_crore",
    "pe_ratio",
    "return_on_equity_pct",
    "composite_quality_score"
]

st.dataframe(
    sector_df[columns],
    use_container_width=True,
    hide_index=True
)

