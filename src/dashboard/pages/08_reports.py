import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import get_report_data

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="Reports & Insights",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Reports & Insights")
st.markdown("Executive summary of the Nifty100 Financial Intelligence Platform.")

# -------------------------------------------------------
# Load Data
# -------------------------------------------------------

df = get_report_data()

if df.empty:
    st.warning("No data available.")
    st.stop()

# -------------------------------------------------------
# Clean Data
# -------------------------------------------------------

numeric_cols = [
    "market_cap_crore",
    "enterprise_value_crore",
    "pe_ratio",
    "pb_ratio",
    "ev_ebitda",
    "dividend_yield_pct",
    "roe_pct",
    "revenue_cagr_pct",
    "debt_to_equity",
    "composite_quality_score"
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# -------------------------------------------------------
# Executive Summary
# -------------------------------------------------------

st.subheader("📌 Executive Summary")

total_companies = df["company_id"].nunique()
total_sectors = df["broad_sector"].nunique()
total_market_cap = df["market_cap_crore"].sum()
avg_roe = df["roe_pct"].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Companies",
        total_companies
    )

with col2:
    st.metric(
        "Sectors",
        total_sectors
    )

with col3:
    st.metric(
        "Total Market Cap",
        f"₹{total_market_cap:,.0f} Cr"
    )

with col4:
    st.metric(
        "Average ROE",
        f"{avg_roe:.2f}%"
    )

# -------------------------------------------------------
# Top Companies
# -------------------------------------------------------

st.markdown("---")
st.subheader("🏆 Top 5 Companies by Market Capitalization")

top5 = (
    df.sort_values(
        "market_cap_crore",
        ascending=False
    )
    .head(5)
)

st.dataframe(
    top5[
        [
            "company_id",
            "broad_sector",
            "market_cap_crore",
            "pe_ratio",
            "roe_pct",
            "composite_quality_score"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# -------------------------------------------------------
# Top 5 Market Cap Chart
# -------------------------------------------------------

fig = px.bar(
    top5,
    x="company_id",
    y="market_cap_crore",
    color="broad_sector",
    text="market_cap_crore",
    title="Top 5 Companies by Market Capitalization"
)

fig.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

fig.update_layout(
    height=550,
    xaxis_title="Company",
    yaxis_title="Market Cap (₹ Crore)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------------
# Best Performing Sector
# -------------------------------------------------------

st.markdown("---")
st.subheader("🥇 Best Performing Sector")

sector_summary = (
    df.groupby("broad_sector")
      .agg(
          Companies=("company_id", "count"),
          Market_Cap=("market_cap_crore", "sum"),
          Average_ROE=("roe_pct", "mean"),
          Average_PE=("pe_ratio", "mean"),
          Average_Quality=("composite_quality_score", "mean")
      )
      .reset_index()
)

sector_summary = sector_summary.sort_values(
    "Average_Quality",
    ascending=False
)

best_sector = sector_summary.iloc[0]

col1, col2 = st.columns([1, 2])

with col1:

    st.success("🏆 Best Sector")

    st.metric(
        "Sector",
        best_sector["broad_sector"]
    )

    st.metric(
        "Quality Score",
        f"{best_sector['Average_Quality']:.2f}"
    )

    st.metric(
        "Average ROE",
        f"{best_sector['Average_ROE']:.2f}%"
    )

with col2:

    st.dataframe(
        sector_summary,
        use_container_width=True,
        hide_index=True
    )

# -------------------------------------------------------
# Sector-wise Market Cap Distribution
# -------------------------------------------------------

st.markdown("---")
st.subheader("📊 Sector-wise Market Capitalization")

fig = px.pie(
    sector_summary,
    names="broad_sector",
    values="Market_Cap",
    hole=0.55,
    title="Sector Contribution to Total Market Capitalization"
)

fig.update_layout(
    height=550
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------------
# Top Performers
# -------------------------------------------------------

st.markdown("---")
st.subheader("⭐ Top Performers")

col1, col2, col3 = st.columns(3)

# Highest ROE
with col1:

    roe_company = (
        df.sort_values(
            "roe_pct",
            ascending=False
        )
        .iloc[0]
    )

    st.info("Highest ROE")

    st.metric(
        roe_company["company_id"],
        f"{roe_company['roe_pct']:.2f}%"
    )

# Lowest Debt
with col2:

    debt_company = (
        df.sort_values(
            "debt_to_equity"
        )
        .iloc[0]
    )

    st.info("Lowest Debt to Equity")

    st.metric(
        debt_company["company_id"],
        f"{debt_company['debt_to_equity']:.2f}"
    )

# Highest Quality
with col3:

    quality_company = (
        df.sort_values(
            "composite_quality_score",
            ascending=False
        )
        .iloc[0]
    )

    st.info("Highest Quality Score")

    st.metric(
        quality_company["company_id"],
        f"{quality_company['composite_quality_score']:.2f}"
    )

# -------------------------------------------------------
# Top Companies by Quality
# -------------------------------------------------------

st.markdown("---")
st.subheader("🌟 Top 10 Companies by Quality Score")

quality_df = (
    df.sort_values(
        "composite_quality_score",
        ascending=False
    )
    .head(10)
)

fig = px.bar(
    quality_df,
    x="company_id",
    y="composite_quality_score",
    color="broad_sector",
    text="composite_quality_score",
    title="Top 10 Companies by Composite Quality Score"
)

fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig.update_layout(
    height=550,
    xaxis_title="Company",
    yaxis_title="Quality Score"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------------
# Portfolio Health Summary
# -------------------------------------------------------

st.markdown("---")
st.subheader("📈 Portfolio Health Summary")

avg_pe = df["pe_ratio"].mean()
avg_pb = df["pb_ratio"].mean()
avg_debt = df["debt_to_equity"].mean()
avg_quality = df["composite_quality_score"].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average P/E",
        f"{avg_pe:.2f}"
    )

with col2:
    st.metric(
        "Average P/B",
        f"{avg_pb:.2f}"
    )

with col3:
    st.metric(
        "Average Debt/Equity",
        f"{avg_debt:.2f}"
    )

with col4:
    st.metric(
        "Average Quality",
        f"{avg_quality:.2f}"
    )

# -------------------------------------------------------
# Automated Insights
# -------------------------------------------------------

st.markdown("---")
st.subheader("💡 Key Insights")

largest_company = df.loc[df["market_cap_crore"].idxmax()]
best_quality = df.loc[df["composite_quality_score"].idxmax()]
highest_roe = df.loc[df["roe_pct"].idxmax()]
lowest_debt = df.loc[df["debt_to_equity"].idxmin()]

st.success(
    f"🏆 **Largest Company:** {largest_company['company_id']} "
    f"(₹{largest_company['market_cap_crore']:,.0f} Cr)"
)

st.success(
    f"⭐ **Highest Quality Company:** {best_quality['company_id']} "
    f"(Score: {best_quality['composite_quality_score']:.2f})"
)

st.success(
    f"📈 **Highest ROE:** {highest_roe['company_id']} "
    f"({highest_roe['roe_pct']:.2f}%)"
)

st.success(
    f"💰 **Lowest Debt-to-Equity:** {lowest_debt['company_id']} "
    f"({lowest_debt['debt_to_equity']:.2f})"
)

# -------------------------------------------------------
# Complete Report Table
# -------------------------------------------------------

st.markdown("---")
st.subheader("📋 Complete Company Report")

report_df = df[[
    "company_id",
    "broad_sector",
    "market_cap_crore",
    "pe_ratio",
    "pb_ratio",
    "roe_pct",
    "debt_to_equity",
    "composite_quality_score"
]].sort_values(
    "market_cap_crore",
    ascending=False
)

report_df = report_df.rename(columns={
    "company_id": "Company",
    "broad_sector": "Sector",
    "market_cap_crore": "Market Cap (Cr)",
    "pe_ratio": "P/E",
    "pb_ratio": "P/B",
    "roe_pct": "ROE (%)",
    "debt_to_equity": "Debt/Equity",
    "composite_quality_score": "Quality Score"
})

st.dataframe(
    report_df,
    use_container_width=True,
    hide_index=True
)

# -------------------------------------------------------
# Download Report
# -------------------------------------------------------

st.markdown("---")

csv = report_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Reports & Insights",
    data=csv,
    file_name="reports_and_insights.csv",
    mime="text/csv"
)

# -------------------------------------------------------
# Footer
# -------------------------------------------------------

st.markdown("---")

st.caption(
    "Nifty100 Financial Intelligence Platform | "
    "Built with Streamlit, Plotly, MySQL & SQLAlchemy"
)