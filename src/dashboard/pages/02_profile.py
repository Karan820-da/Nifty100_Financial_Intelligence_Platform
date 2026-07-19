import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import get_base_data

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Company Profile",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Company Profile")

st.caption("Detailed financial analysis for an individual company.")

# --------------------------------------------------
# Load Data
# --------------------------------------------------

df = get_base_data()

if df.empty:
    st.error("No data available.")
    st.stop()

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.header("Company Selection")

companies = sorted(df["company_id"].dropna().unique())

selected_company = st.sidebar.selectbox(
    "Select Company",
    companies
)

company_df = df[
    df["company_id"] == selected_company
].copy()

if company_df.empty:
    st.warning("Company data not found.")
    st.stop()

# Latest Record

latest = (
    company_df
    .sort_values("year")
    .iloc[-1]
)

# --------------------------------------------------
# Company Overview
# --------------------------------------------------

st.subheader(selected_company)

col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        f"""
**Sector**

{latest['broad_sector']}
"""
    )

with col2:
    st.info(
        f"""
**Sub Sector**

{latest['sub_sector']}
"""
    )

with col3:
    st.info(
        f"""
**Market Cap Category**

{latest['market_cap_category']}
"""
    )

st.markdown("---")

# --------------------------------------------------
# Key Performance Indicators
# --------------------------------------------------

st.subheader("📊 Key Financial Metrics")

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

with col1:
    st.metric(
        "💰 Market Cap",
        f"₹ {latest['market_cap_crore']:,.0f} Cr"
        if pd.notna(latest["market_cap_crore"])
        else "N/A"
    )

with col2:
    st.metric(
        "📈 PE Ratio",
        f"{latest['pe_ratio']:.2f}"
        if pd.notna(latest["pe_ratio"])
        else "N/A"
    )

with col3:
    st.metric(
        "📚 PB Ratio",
        f"{latest['pb_ratio']:.2f}"
        if pd.notna(latest["pb_ratio"])
        else "N/A"
    )

with col4:
    st.metric(
        "📊 ROE",
        f"{latest['return_on_equity_pct']:.2f}%"
        if pd.notna(latest["return_on_equity_pct"])
        else "N/A"
    )

with col5:
    st.metric(
        "🏦 Debt / Equity",
        f"{latest['debt_to_equity']:.2f}"
        if pd.notna(latest["debt_to_equity"])
        else "N/A"
    )

with col6:
    st.metric(
        "⭐ Quality Score",
        f"{latest['composite_quality_score']:.2f}"
        if pd.notna(latest["composite_quality_score"])
        else "N/A"
    )

st.markdown("---")

# --------------------------------------------------
# Growth Metrics
# --------------------------------------------------

st.subheader("📈 Growth Metrics")

gcol1, gcol2, gcol3, gcol4 = st.columns(4)

with gcol1:
    st.metric(
        "Revenue CAGR (5Y)",
        f"{latest['revenue_cagr_5yr']:.2f}%"
        if pd.notna(latest["revenue_cagr_5yr"])
        else "N/A"
    )

with gcol2:
    st.metric(
        "PAT CAGR (5Y)",
        f"{latest['pat_cagr_5yr']:.2f}%"
        if pd.notna(latest["pat_cagr_5yr"])
        else "N/A"
    )

with gcol3:
    st.metric(
        "EPS CAGR (5Y)",
        f"{latest['eps_cagr_5yr']:.2f}%"
        if pd.notna(latest["eps_cagr_5yr"])
        else "N/A"
    )

with gcol4:
    st.metric(
        "Dividend Yield",
        f"{latest['dividend_yield_pct']:.2f}%"
        if pd.notna(latest["dividend_yield_pct"])
        else "N/A"
    )

st.markdown("---")

# --------------------------------------------------
# Key Performance Indicators
# --------------------------------------------------

st.subheader("📊 Key Financial Metrics")

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

with col1:
    st.metric(
        "💰 Market Cap",
        f"₹ {latest['market_cap_crore']:,.0f} Cr"
        if pd.notna(latest["market_cap_crore"])
        else "N/A"
    )

with col2:
    st.metric(
        "📈 PE Ratio",
        f"{latest['pe_ratio']:.2f}"
        if pd.notna(latest["pe_ratio"])
        else "N/A"
    )

with col3:
    st.metric(
        "📚 PB Ratio",
        f"{latest['pb_ratio']:.2f}"
        if pd.notna(latest["pb_ratio"])
        else "N/A"
    )

with col4:
    st.metric(
        "📊 ROE",
        f"{latest['return_on_equity_pct']:.2f}%"
        if pd.notna(latest["return_on_equity_pct"])
        else "N/A"
    )

with col5:
    st.metric(
        "🏦 Debt / Equity",
        f"{latest['debt_to_equity']:.2f}"
        if pd.notna(latest["debt_to_equity"])
        else "N/A"
    )

with col6:
    st.metric(
        "⭐ Quality Score",
        f"{latest['composite_quality_score']:.2f}"
        if pd.notna(latest["composite_quality_score"])
        else "N/A"
    )

st.markdown("---")

# --------------------------------------------------
# Growth Metrics
# --------------------------------------------------

st.subheader("📈 Growth Metrics")

gcol1, gcol2, gcol3, gcol4 = st.columns(4)

with gcol1:
    st.metric(
        "Revenue CAGR (5Y)",
        f"{latest['revenue_cagr_5yr']:.2f}%"
        if pd.notna(latest["revenue_cagr_5yr"])
        else "N/A"
    )

with gcol2:
    st.metric(
        "PAT CAGR (5Y)",
        f"{latest['pat_cagr_5yr']:.2f}%"
        if pd.notna(latest["pat_cagr_5yr"])
        else "N/A"
    )

with gcol3:
    st.metric(
        "EPS CAGR (5Y)",
        f"{latest['eps_cagr_5yr']:.2f}%"
        if pd.notna(latest["eps_cagr_5yr"])
        else "N/A"
    )

with gcol4:
    st.metric(
        "Dividend Yield",
        f"{latest['dividend_yield_pct']:.2f}%"
        if pd.notna(latest["dividend_yield_pct"])
        else "N/A"
    )

st.markdown("---")

# --------------------------------------------------
# Historical Trend Analysis
# --------------------------------------------------

st.subheader("📈 Historical Performance")

# Ensure chronological order
trend_df = company_df.copy()
trend_df["year"] = trend_df["year"].astype(int)
trend_df = trend_df.sort_values("year")

# --------------------------------------------------
# Row 1
# --------------------------------------------------

chart_col1, chart_col2 = st.columns(2)

# Market Cap Trend
fig_marketcap = px.line(
    trend_df,
    x="year",
    y="market_cap_crore",
    markers=True,
    title="Market Capitalization Trend"
)

fig_marketcap.update_layout(
    xaxis_title="Year",
    yaxis_title="Market Cap (₹ Cr)",
    height=400
)

with chart_col1:
    st.plotly_chart(fig_marketcap, use_container_width=True)

# ROE Trend
fig_roe = px.line(
    trend_df,
    x="year",
    y="return_on_equity_pct",
    markers=True,
    title="Return on Equity (ROE)"
)

fig_roe.update_layout(
    xaxis_title="Year",
    yaxis_title="ROE (%)",
    height=400
)

with chart_col2:
    st.plotly_chart(fig_roe, use_container_width=True)

# --------------------------------------------------
# Row 2
# --------------------------------------------------

chart_col3, chart_col4 = st.columns(2)

# PE Ratio Trend
fig_pe = px.line(
    trend_df,
    x="year",
    y="pe_ratio",
    markers=True,
    title="PE Ratio Trend"
)

fig_pe.update_layout(
    xaxis_title="Year",
    yaxis_title="PE Ratio",
    height=400
)

with chart_col3:
    st.plotly_chart(fig_pe, use_container_width=True)

# Revenue CAGR Trend
fig_revenue = px.line(
    trend_df,
    x="year",
    y="revenue_cagr_5yr",
    markers=True,
    title="Revenue CAGR (5Y)"
)

fig_revenue.update_layout(
    xaxis_title="Year",
    yaxis_title="Revenue CAGR (%)",
    height=400
)

with chart_col4:
    st.plotly_chart(fig_revenue, use_container_width=True)

st.markdown("---")

# --------------------------------------------------
# Financial Ratios Table
# --------------------------------------------------

st.subheader("📋 Financial Ratios")

display_columns = [
    "year",
    "market_cap_crore",
    "pe_ratio",
    "pb_ratio",
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "eps_cagr_5yr",
    "dividend_yield_pct",
    "composite_quality_score"
]

ratio_df = company_df[display_columns].copy()

ratio_df = ratio_df.rename(columns={
    "year": "Year",
    "market_cap_crore": "Market Cap (₹ Cr)",
    "pe_ratio": "PE Ratio",
    "pb_ratio": "PB Ratio",
    "return_on_equity_pct": "ROE (%)",
    "debt_to_equity": "Debt/Equity",
    "revenue_cagr_5yr": "Revenue CAGR (5Y %)",
    "pat_cagr_5yr": "PAT CAGR (5Y %)",
    "eps_cagr_5yr": "EPS CAGR (5Y %)",
    "dividend_yield_pct": "Dividend Yield (%)",
    "composite_quality_score": "Quality Score"
})

st.dataframe(
    ratio_df,
    use_container_width=True,
    hide_index=True,
    height=350
)

# --------------------------------------------------
# Company Summary
# --------------------------------------------------

st.subheader("📝 Company Snapshot")

summary_col1, summary_col2 = st.columns(2)

with summary_col1:

    st.success(f"""
### {selected_company}

**Sector:** {latest['broad_sector']}

**Sub Sector:** {latest['sub_sector']}

**Market Cap Category:** {latest['market_cap_category']}
""")

with summary_col2:

    st.info(f"""
### Financial Highlights

⭐ Quality Score : **{latest['composite_quality_score']:.2f}**

📈 ROE : **{latest['return_on_equity_pct']:.2f}%**

📊 PE Ratio : **{latest['pe_ratio']:.2f}**

💰 Dividend Yield : **{latest['dividend_yield_pct']:.2f}%**
""")

# --------------------------------------------------
# Download Company Report
# --------------------------------------------------

csv = company_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Company Data",
    data=csv,
    file_name=f"{selected_company}_financial_data.csv",
    mime="text/csv"
)

st.markdown("---")

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown("""
<style>

div[data-testid="metric-container"]{
    background:#f8f9fa;
    border-radius:12px;
    padding:15px;
    border:1px solid #e5e5e5;
}

.block-container{
    padding-top:2rem;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.caption(
    "Nifty100 Financial Intelligence Platform | Company Profile Dashboard"
)