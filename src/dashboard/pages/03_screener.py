import streamlit as st
import pandas as pd

from utils.db import get_screener_data

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Stock Screener",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Stock Screener")

st.caption(
    "Filter Nifty100 companies using financial and valuation metrics."
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------

df = get_screener_data()

if df.empty:
    st.error("No data available.")
    st.stop()

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------

st.sidebar.header("Screening Filters")

# Sector

sector_options = ["All"] + sorted(
    df["broad_sector"].dropna().unique().tolist()
)

selected_sector = st.sidebar.selectbox(
    "Sector",
    sector_options
)

# Market Cap Category

cap_options = ["All"] + sorted(
    df["market_cap_category"].dropna().unique().tolist()
)

selected_cap = st.sidebar.selectbox(
    "Market Cap Category",
    cap_options
)

# ROE

min_roe = st.sidebar.slider(
    "Minimum ROE (%)",
    min_value=0.0,
    max_value=float(df["return_on_equity_pct"].max()),
    value=10.0
)

# PE

max_pe = st.sidebar.slider(
    "Maximum PE Ratio",
    min_value=0.0,
    max_value=float(df["pe_ratio"].max()),
    value=float(df["pe_ratio"].max())
)

# Debt

max_debt = st.sidebar.slider(
    "Maximum Debt/Equity",
    min_value=0.0,
    max_value=float(df["debt_to_equity"].max()),
    value=float(df["debt_to_equity"].max())
)

# Quality

min_quality = st.sidebar.slider(
    "Minimum Quality Score",
    min_value=0.0,
    max_value=100.0,
    value=50.0
)

# --------------------------------------------------
# Apply Filters
# --------------------------------------------------

filtered_df = df.copy()

if selected_sector != "All":
    filtered_df = filtered_df[
        filtered_df["broad_sector"] == selected_sector
    ]

if selected_cap != "All":
    filtered_df = filtered_df[
        filtered_df["market_cap_category"] == selected_cap
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

if filtered_df.empty:
    st.warning("No companies match the selected filters.")
    st.stop()

# --------------------------------------------------
# Screener Summary
# --------------------------------------------------

st.markdown("## 📊 Screening Results")

total_companies = filtered_df["company_id"].nunique()

avg_roe = filtered_df["return_on_equity_pct"].mean()

avg_pe = filtered_df["pe_ratio"].mean()

avg_quality = filtered_df["composite_quality_score"].mean()

total_market_cap = filtered_df["market_cap_crore"].sum()

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.metric(
        "🏢 Companies",
        total_companies
    )

with kpi2:
    st.metric(
        "💰 Total Market Cap",
        f"₹ {total_market_cap:,.0f} Cr"
        if pd.notna(total_market_cap)
        else "N/A"
    )

with kpi3:
    st.metric(
        "📈 Avg ROE",
        f"{avg_roe:.2f}%"
        if pd.notna(avg_roe)
        else "N/A"
    )

with kpi4:
    st.metric(
        "📊 Avg PE",
        f"{avg_pe:.2f}"
        if pd.notna(avg_pe)
        else "N/A"
    )

with kpi5:
    st.metric(
        "⭐ Avg Quality",
        f"{avg_quality:.2f}"
        if pd.notna(avg_quality)
        else "N/A"
    )

st.markdown("---")

# --------------------------------------------------
# Top Companies
# --------------------------------------------------

st.subheader("🏆 Top Matching Companies")

top_companies = (
    filtered_df
    .sort_values(
        by=[
            "composite_quality_score",
            "return_on_equity_pct"
        ],
        ascending=False
    )
    .head(10)
)

display_top = top_companies[
    [
        "company_id",
        "broad_sector",
        "market_cap_crore",
        "return_on_equity_pct",
        "pe_ratio",
        "debt_to_equity",
        "composite_quality_score"
    ]
].copy()

display_top.columns = [
    "Company",
    "Sector",
    "Market Cap (₹ Cr)",
    "ROE (%)",
    "PE",
    "Debt/Equity",
    "Quality Score"
]

st.dataframe(
    display_top,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# --------------------------------------------------
# Smart Investment Score
# --------------------------------------------------

ranking_df = filtered_df.copy()

# Fill missing values

score_columns = [
    "composite_quality_score",
    "return_on_equity_pct",
    "revenue_cagr_5yr",
    "debt_to_equity"
]

for col in score_columns:
    ranking_df[col] = ranking_df[col].fillna(0)

# Normalize Metrics

ranking_df["quality_norm"] = (
    ranking_df["composite_quality_score"] /
    ranking_df["composite_quality_score"].max()
)

ranking_df["roe_norm"] = (
    ranking_df["return_on_equity_pct"] /
    ranking_df["return_on_equity_pct"].max()
)

ranking_df["growth_norm"] = (
    ranking_df["revenue_cagr_5yr"] /
    ranking_df["revenue_cagr_5yr"].max()
)

# Lower Debt = Better Score

max_debt = ranking_df["debt_to_equity"].max()

if max_debt == 0:
    ranking_df["debt_norm"] = 1
else:
    ranking_df["debt_norm"] = (
        1 -
        (ranking_df["debt_to_equity"] / max_debt)
    )

# --------------------------------------------------
# Weighted Smart Score
# --------------------------------------------------

ranking_df["smart_score"] = (

    ranking_df["quality_norm"] * 0.40 +

    ranking_df["roe_norm"] * 0.30 +

    ranking_df["growth_norm"] * 0.20 +

    ranking_df["debt_norm"] * 0.10

) * 100

ranking_df["smart_score"] = ranking_df["smart_score"].round(2)

# --------------------------------------------------
# Top Investment Picks
# --------------------------------------------------

st.subheader("🏆 AI Top Investment Picks")

top_picks = (
    ranking_df
    .sort_values(
        "smart_score",
        ascending=False
    )
    .head(10)
)

display_columns = [

    "company_id",
    "broad_sector",
    "market_cap_crore",

    "return_on_equity_pct",
    "pe_ratio",

    "debt_to_equity",

    "revenue_cagr_5yr",

    "composite_quality_score",

    "smart_score"

]

top_display = top_picks[display_columns].copy()

top_display.columns = [

    "Company",
    "Sector",
    "Market Cap (₹ Cr)",

    "ROE (%)",
    "PE Ratio",

    "Debt / Equity",

    "Revenue CAGR (%)",

    "Quality Score",

    "Smart Score"

]

st.dataframe(
    top_display,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# Highlight Best Company
# --------------------------------------------------

best = top_picks.iloc[0]

st.success(
    f"""
🥇 **Best Matching Company**

**{best['company_id']}**

⭐ Smart Score : **{best['smart_score']:.2f}**

📈 ROE : **{best['return_on_equity_pct']:.2f}%**

📊 PE Ratio : **{best['pe_ratio']:.2f}**

🚀 Revenue CAGR : **{best['revenue_cagr_5yr']:.2f}%**
"""
)

st.markdown("---")

# --------------------------------------------------
# Ranking Charts
# --------------------------------------------------

import plotly.express as px

st.subheader("📊 Screening Insights")

chart_col1, chart_col2 = st.columns(2)

# Top Smart Score

fig_score = px.bar(
    top_picks,
    x="company_id",
    y="smart_score",
    color="smart_score",
    text_auto=".2f",
    title="Top Companies by Smart Score"
)

fig_score.update_layout(
    xaxis_title="Company",
    yaxis_title="Smart Score",
    height=450
)

with chart_col1:
    st.plotly_chart(
        fig_score,
        use_container_width=True
    )

# ROE vs PE

fig_scatter = px.scatter(

    ranking_df,

    x="pe_ratio",
    y="return_on_equity_pct",

    color="broad_sector",

    size="market_cap_crore",

    hover_name="company_id",

    title="PE Ratio vs ROE"

)

fig_scatter.update_layout(height=450)

with chart_col2:
    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )

st.markdown("---")

# --------------------------------------------------
# Complete Screener Table
# --------------------------------------------------

st.subheader("📋 Filtered Companies")

display_df = ranking_df[

    [

        "company_id",

        "broad_sector",

        "market_cap_category",

        "market_cap_crore",

        "return_on_equity_pct",

        "pe_ratio",

        "pb_ratio",

        "debt_to_equity",

        "revenue_cagr_5yr",

        "composite_quality_score",

        "smart_score"

    ]

].copy()

display_df.columns = [

    "Company",

    "Sector",

    "Market Cap Category",

    "Market Cap (₹ Cr)",

    "ROE (%)",

    "PE",

    "PB",

    "Debt/Equity",

    "Revenue CAGR (%)",

    "Quality Score",

    "Smart Score"

]

display_df = display_df.sort_values(
    "Smart Score",
    ascending=False
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    height=550
)

# --------------------------------------------------
# Download CSV
# --------------------------------------------------

csv = display_df.to_csv(index=False).encode("utf-8")

st.download_button(

    "⬇ Download Screening Results",

    csv,

    "screening_results.csv",

    "text/csv"

)

st.markdown("---")

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.caption(
    "Nifty100 Financial Intelligence Platform | Stock Screener"
)