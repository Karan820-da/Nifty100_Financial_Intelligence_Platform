import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import get_sector_data

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="Sector Analysis",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Sector Analysis")

st.markdown(
    """
Analyze the latest financial performance across different sectors of the Nifty 100 companies.
    """
)

# -------------------------------------------------------
# Load Data
# -------------------------------------------------------

df = get_sector_data()

# -------------------------------------------------------
# Remove Missing Sectors
# -------------------------------------------------------

df = df.dropna(subset=["broad_sector"])

# -------------------------------------------------------
# KPI Cards
# -------------------------------------------------------

total_sectors = df["broad_sector"].nunique()
total_companies = df["company_id"].nunique()

avg_roe = df["return_on_equity_pct"].mean()

best_sector = (
    df.groupby("broad_sector")["return_on_equity_pct"]
      .mean()
      .idxmax()
)

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sectors",
    total_sectors
)

col2.metric(
    "Companies",
    total_companies
)

col3.metric(
    "Best Sector",
    best_sector
)

col4.metric(
    "Average ROE",
    f"{avg_roe:.2f}%"
)

# -------------------------------------------------------
# Sector Distribution
# -------------------------------------------------------

st.markdown("---")

st.subheader("🥧 Sector Distribution")

sector_count = (
    df.groupby("broad_sector")
      .size()
      .reset_index(name="Companies")
)

fig = px.pie(
    sector_count,
    names="broad_sector",
    values="Companies",
    hole=0.5,
    title="Companies by Sector"
)

fig.update_layout(
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------------
# Sector Summary Table
# -------------------------------------------------------

st.markdown("---")

st.subheader("📋 Sector Summary")

sector_summary = (
    df.groupby("broad_sector")
      .agg(
          Companies=("company_id", "count"),
          Average_ROE=("return_on_equity_pct", "mean"),
          Average_PE=("pe_ratio", "mean"),
          Average_Debt=("debt_to_equity", "mean"),
          Average_CAGR=("revenue_cagr_5yr", "mean"),
          Average_Quality=("composite_quality_score", "mean")
      )
      .reset_index()
)

sector_summary = sector_summary.rename(
    columns={
        "broad_sector": "Sector",
        "Average_ROE": "Average ROE (%)",
        "Average_PE": "Average P/E",
        "Average_Debt": "Average Debt/Equity",
        "Average_CAGR": "Average Revenue CAGR (%)",
        "Average_Quality": "Average Quality Score"
    }
)
# -------------------------------------------------------
# Sector Performance Charts
# -------------------------------------------------------

st.markdown("---")

st.subheader("📊 Sector Performance Dashboard")

col1, col2 = st.columns(2)

# -------------------------------------------------------
# Average ROE by Sector
# -------------------------------------------------------

with col1:

    roe_chart = sector_summary.sort_values(
        "Average ROE (%)",
        ascending=False
    )

    fig = px.bar(
        roe_chart,
        x="Sector",
        y="Average ROE (%)",
        text="Average ROE (%)",
        title="Average ROE by Sector"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Sector",
        yaxis_title="Average ROE (%)",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -------------------------------------------------------
# Average P/E Ratio by Sector
# -------------------------------------------------------

with col2:

    pe_chart = sector_summary.sort_values(
        "Average P/E",
        ascending=False
    )

    fig = px.bar(
        pe_chart,
        x="Sector",
        y="Average P/E",
        text="Average P/E",
        title="Average P/E Ratio by Sector"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Sector",
        yaxis_title="Average P/E",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -------------------------------------------------------
# Revenue CAGR & Quality Score
# -------------------------------------------------------

col3, col4 = st.columns(2)

# Revenue CAGR

with col3:

    cagr_chart = sector_summary.sort_values(
        "Average Revenue CAGR (%)",
        ascending=False
    )

    fig = px.bar(
        cagr_chart,
        x="Sector",
        y="Average Revenue CAGR (%)",
        text="Average Revenue CAGR (%)",
        title="Average Revenue CAGR by Sector"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Sector",
        yaxis_title="Revenue CAGR (%)",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# Quality Score

with col4:

    quality_chart = sector_summary.sort_values(
        "Average Quality Score",
        ascending=False
    )

    fig = px.bar(
        quality_chart,
        x="Sector",
        y="Average Quality Score",
        text="Average Quality Score",
        title="Average Quality Score by Sector"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Sector",
        yaxis_title="Quality Score",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.dataframe(
    sector_summary,
    use_container_width=True,
    hide_index=True
)

# -------------------------------------------------------
# Top Company in Each Sector
# -------------------------------------------------------

st.markdown("---")

st.subheader("🏆 Top Company in Each Sector")

top_company = (
    df.sort_values(
        "composite_quality_score",
        ascending=False
    )
    .groupby("broad_sector")
    .first()
    .reset_index()
)

top_company = top_company[
    [
        "broad_sector",
        "company_id",
        "return_on_equity_pct",
        "pe_ratio",
        "composite_quality_score"
    ]
]

top_company = top_company.rename(
    columns={
        "broad_sector": "Sector",
        "company_id": "Top Company",
        "return_on_equity_pct": "ROE (%)",
        "pe_ratio": "P/E Ratio",
        "composite_quality_score": "Quality Score"
    }
)

st.dataframe(
    top_company,
    use_container_width=True,
    hide_index=True
)

# -------------------------------------------------------
# Sector Ranking
# -------------------------------------------------------

st.markdown("---")

st.subheader("🥇 Sector Ranking")

ranking = sector_summary.sort_values(
    "Average Quality Score",
    ascending=False
).reset_index(drop=True)

ranking.index = ranking.index + 1

st.dataframe(
    ranking,
    use_container_width=True
)

# -------------------------------------------------------
# Best Performing Sector
# -------------------------------------------------------

st.markdown("---")

best_sector_row = ranking.iloc[0]

st.success(
    f"""
🏆 Best Performing Sector: **{best_sector_row['Sector']}**

• Average Quality Score: **{best_sector_row['Average Quality Score']:.2f}**

• Average ROE: **{best_sector_row['Average ROE (%)']:.2f}%**
"""
)

# -------------------------------------------------------
# Download Report
# -------------------------------------------------------

st.markdown("---")

csv = sector_summary.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Sector Report",
    data=csv,
    file_name="sector_analysis_report.csv",
    mime="text/csv"
)