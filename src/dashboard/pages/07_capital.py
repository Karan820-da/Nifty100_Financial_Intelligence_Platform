import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import get_capital_data

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="Capital Allocation",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Capital Allocation Dashboard")

st.markdown("""
Analyze the latest market capitalization and capital allocation across Nifty 100 companies.
""")

# -------------------------------------------------------
# Load Data
# -------------------------------------------------------

df = get_capital_data()

# Remove companies with missing Market Cap
df = df.dropna(subset=["market_cap_crore"])

# -------------------------------------------------------
# KPI Cards
# -------------------------------------------------------

total_market_cap = df["market_cap_crore"].sum()

largest_company = df.loc[
    df["market_cap_crore"].idxmax(),
    "company_id"
]

average_pe = df["pe_ratio"].mean()

average_quality = df["composite_quality_score"].mean()

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Market Cap",
    f"₹{total_market_cap:,.0f} Cr"
)

col2.metric(
    "Largest Company",
    largest_company
)

col3.metric(
    "Average P/E",
    f"{average_pe:.2f}"
)

col4.metric(
    "Average Quality",
    f"{average_quality:.2f}"
)

# -------------------------------------------------------
# Top 10 Companies
# -------------------------------------------------------

st.markdown("---")

st.subheader("🏆 Top 10 Companies by Market Capitalization")

top10 = (
    df.sort_values(
        "market_cap_crore",
        ascending=False
    )
    .head(10)
)

table = top10[
    [
        "company_id",
        "broad_sector",
        "market_cap_crore",
        "pe_ratio",
        "composite_quality_score"
    ]
].rename(
    columns={
        "company_id": "Company",
        "broad_sector": "Sector",
        "market_cap_crore": "Market Cap (Cr)",
        "pe_ratio": "P/E Ratio",
        "composite_quality_score": "Quality Score"
    }
)

st.dataframe(
    table,
    use_container_width=True,
    hide_index=True
)

# -------------------------------------------------------
# Market Cap Bar Chart
# -------------------------------------------------------

st.markdown("---")

st.subheader("📊 Top 10 Market Capitalization")

fig = px.bar(
    table,
    x="Company",
    y="Market Cap (Cr)",
    text="Market Cap (Cr)",
    color="Sector",
    title="Top 10 Companies by Market Capitalization"
)

fig.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

fig.update_layout(
    height=600,
    xaxis_title="Company",
    yaxis_title="Market Cap (Crore)",
    legend_title="Sector"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------------
# Market Cap vs P/E Ratio
# -------------------------------------------------------

st.markdown("---")

st.subheader("📈 Market Capitalization vs P/E Ratio")

scatter_df = df.dropna(
    subset=["market_cap_crore", "pe_ratio"]
)

fig = px.scatter(
    scatter_df,
    x="market_cap_crore",
    y="pe_ratio",
    color="broad_sector",
    size="market_cap_crore",
    hover_name="company_id",
    title="Market Cap vs P/E Ratio"
)

fig.update_layout(
    height=650,
    xaxis_title="Market Capitalization (Crore)",
    yaxis_title="P/E Ratio",
    legend_title="Sector"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------------
# Sector-wise Market Capitalization
# -------------------------------------------------------

st.markdown("---")

st.subheader("🏭 Sector-wise Market Capitalization")

sector_cap = (
    df.groupby("broad_sector")
      .agg(
          Total_Market_Cap=("market_cap_crore", "sum")
      )
      .reset_index()
      .sort_values(
          "Total_Market_Cap",
          ascending=False
      )
)

col1, col2 = st.columns(2)

# Bar Chart
with col1:

    fig = px.bar(
        sector_cap,
        x="broad_sector",
        y="Total_Market_Cap",
        text="Total_Market_Cap",
        title="Market Cap by Sector"
    )

    fig.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside"
    )

    fig.update_layout(
        height=500,
        xaxis_title="Sector",
        yaxis_title="Market Cap (Crore)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# Donut Chart
with col2:

    fig = px.pie(
        sector_cap,
        names="broad_sector",
        values="Total_Market_Cap",
        hole=0.55,
        title="Sector Market Cap Distribution"
    )

    fig.update_layout(
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -------------------------------------------------------
# Capital Allocation Summary
# -------------------------------------------------------

st.markdown("---")

st.subheader("📋 Capital Allocation Summary")

summary = (
    df.groupby("broad_sector")
      .agg(
          Companies=("company_id", "count"),
          Market_Cap=("market_cap_crore", "sum"),
          Avg_PE=("pe_ratio", "mean"),
          Avg_Quality=("composite_quality_score", "mean")
      )
      .reset_index()
)

summary = summary.rename(
    columns={
        "broad_sector": "Sector",
        "Market_Cap": "Market Cap (Cr)",
        "Avg_PE": "Average P/E",
        "Avg_Quality": "Average Quality Score"
    }
)

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)

# -------------------------------------------------------
# Download Report
# -------------------------------------------------------

st.markdown("---")

csv = summary.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Capital Allocation Report",
    data=csv,
    file_name="capital_allocation_report.csv",
    mime="text/csv"
)