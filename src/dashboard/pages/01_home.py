import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import get_home_data

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Nifty100 Financial Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Nifty100 Financial Intelligence Platform")
st.caption("Interactive dashboard for analysing Nifty 100 companies.")

# --------------------------------------------------
# Load Data
# --------------------------------------------------

df = get_home_data()

if df.empty:
    st.warning("No data available.")
    st.stop()

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------

st.sidebar.header("Filters")

# Year Filter
years = sorted(df["year"].dropna().unique(), reverse=True)

selected_year = st.sidebar.selectbox(
    "Select Year",
    years
)

filtered_df = df[df["year"] == selected_year].copy()

# Sector Filter
sectors = ["All"] + sorted(
    filtered_df["broad_sector"].dropna().unique().tolist()
)

selected_sector = st.sidebar.selectbox(
    "Select Sector",
    sectors
)

if selected_sector != "All":
    filtered_df = filtered_df[
        filtered_df["broad_sector"] == selected_sector
    ]

# Company Search
company_search = st.sidebar.text_input(
    "Search Company"
)

if company_search:

    filtered_df = filtered_df[
        filtered_df["company_id"]
        .str.contains(
            company_search,
            case=False,
            na=False
        )
    ]

st.sidebar.markdown("---")
st.sidebar.write(
    f"Showing **{len(filtered_df)}** companies"
)

# --------------------------------------------------
# Data Validation
# --------------------------------------------------

if filtered_df.empty:
    st.warning("No companies match the selected filters.")
    st.stop()

# --------------------------------------------------
# KPI Calculations
# --------------------------------------------------

total_companies = filtered_df["company_id"].nunique()

total_market_cap = filtered_df["market_cap_crore"].sum()

avg_pe = filtered_df["pe_ratio"].mean()

avg_roe = filtered_df["return_on_equity_pct"].mean()

avg_quality = filtered_df["composite_quality_score"].mean()

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

st.markdown("## 📈 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="🏢 Companies",
        value=f"{total_companies}"
    )

with col2:
    st.metric(
        label="💰 Market Cap",
        value=f"₹ {total_market_cap:,.0f} Cr"
    )

with col3:
    st.metric(
        label="📊 Avg PE",
        value=f"{avg_pe:.2f}"
        if pd.notna(avg_pe)
        else "N/A"
    )

with col4:
    st.metric(
        label="📈 Avg ROE",
        value=f"{avg_roe:.2f}%"
        if pd.notna(avg_roe)
        else "N/A"
    )

with col5:
    st.metric(
        label="⭐ Quality Score",
        value=f"{avg_quality:.2f}"
        if pd.notna(avg_quality)
        else "N/A"
    )

st.markdown("---")

# --------------------------------------------------
# Charts
# --------------------------------------------------

st.markdown("## 📊 Market Overview")

# ==========================
# Chart 1 - Market Cap by Sector
# ==========================

sector_marketcap = (
    filtered_df.groupby("broad_sector", as_index=False)["market_cap_crore"]
    .sum()
    .sort_values("market_cap_crore", ascending=False)
)

fig_sector_cap = px.bar(
    sector_marketcap,
    x="broad_sector",
    y="market_cap_crore",
    color="market_cap_crore",
    text_auto=".2s",
    title="Market Capitalization by Sector"
)

fig_sector_cap.update_layout(
    xaxis_title="Sector",
    yaxis_title="Market Cap (₹ Cr)",
    height=450
)

# ==========================
# Chart 2 - Sector Distribution
# ==========================

sector_distribution = (
    filtered_df.groupby("broad_sector", as_index=False)["company_id"]
    .count()
    .rename(columns={"company_id": "Companies"})
)

fig_sector_dist = px.pie(
    sector_distribution,
    names="broad_sector",
    values="Companies",
    hole=0.45,
    title="Company Distribution Across Sectors"
)

fig_sector_dist.update_traces(textinfo="percent+label")

# Display Row 1

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_sector_cap, use_container_width=True)

with col2:
    st.plotly_chart(fig_sector_dist, use_container_width=True)

# --------------------------------------------------
# Row 2 Charts
# --------------------------------------------------

# ==========================
# Chart 3 - Top 10 Companies
# ==========================

top_companies = (
    filtered_df.sort_values(
        "market_cap_crore",
        ascending=False
    )
    .head(10)
)

fig_top = px.bar(
    top_companies.sort_values("market_cap_crore"),
    x="market_cap_crore",
    y="company_id",
    orientation="h",
    color="market_cap_crore",
    text_auto=".2s",
    title="Top 10 Companies by Market Capitalization"
)

fig_top.update_layout(
    xaxis_title="Market Cap (₹ Cr)",
    yaxis_title="Company",
    height=500
)

# ==========================
# Chart 4 - PE vs ROE
# ==========================

scatter_df = filtered_df.dropna(
    subset=[
        "pe_ratio",
        "return_on_equity_pct"
    ]
)

fig_scatter = px.scatter(
    scatter_df,
    x="pe_ratio",
    y="return_on_equity_pct",
    color="broad_sector",
    hover_name="company_id",
    size="market_cap_crore",
    title="PE Ratio vs Return on Equity",
    labels={
        "pe_ratio": "PE Ratio",
        "return_on_equity_pct": "ROE (%)"
    }
)

fig_scatter.update_layout(height=500)

# Display Row 2

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(fig_top, use_container_width=True)

with col4:
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

# --------------------------------------------------
# Company Financial Data
# --------------------------------------------------

st.markdown("## 📋 Company Financial Overview")

table_df = filtered_df[
    [
        "company_id",
        "broad_sector",
        "market_cap_crore",
        "pe_ratio",
        "pb_ratio",
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "composite_quality_score",
    ]
].copy()

# Rename columns for display
table_df.columns = [
    "Company",
    "Sector",
    "Market Cap (₹ Cr)",
    "PE Ratio",
    "PB Ratio",
    "ROE (%)",
    "Debt/Equity",
    "Revenue CAGR 5Y (%)",
    "Quality Score",
]

# Format numeric columns
table_df["Market Cap (₹ Cr)"] = table_df["Market Cap (₹ Cr)"].round(2)
table_df["PE Ratio"] = table_df["PE Ratio"].round(2)
table_df["PB Ratio"] = table_df["PB Ratio"].round(2)
table_df["ROE (%)"] = table_df["ROE (%)"].round(2)
table_df["Debt/Equity"] = table_df["Debt/Equity"].round(2)
table_df["Revenue CAGR 5Y (%)"] = table_df["Revenue CAGR 5Y (%)"].round(2)
table_df["Quality Score"] = table_df["Quality Score"].round(2)

st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=True,
    height=500,
)

# --------------------------------------------------
# Download CSV
# --------------------------------------------------

csv = table_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Data (CSV)",
    data=csv,
    file_name=f"nifty100_{selected_year}.csv",
    mime="text/csv",
)

# --------------------------------------------------
# Dataset Summary
# --------------------------------------------------

st.markdown("## 📊 Dataset Summary")

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:
    st.info(f"**Total Records:** {len(table_df):,}")

with summary_col2:
    st.info(f"**Total Sectors:** {table_df['Sector'].nunique()}")

with summary_col3:
    avg_quality = table_df["Quality Score"].mean()
    st.info(f"**Average Quality Score:** {avg_quality:.2f}")

# --------------------------------------------------
# Custom Styling
# --------------------------------------------------

st.markdown(
    """
    <style>

    .block-container{
        padding-top:2rem;
        padding-bottom:2rem;
        padding-left:2rem;
        padding-right:2rem;
    }

    div[data-testid="metric-container"]{
        background-color:#f8f9fa;
        border:1px solid #e6e6e6;
        padding:15px;
        border-radius:12px;
        box-shadow:0 2px 6px rgba(0,0,0,0.08);
    }

    div[data-testid="metric-container"] label{
        font-weight:600;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown("---")

col1, col2 = st.columns([3, 1])

with col1:
    st.caption(
        "Nifty100 Financial Intelligence Platform | "
        "Built with Streamlit • Plotly • MySQL • SQLAlchemy"
    )

with col2:
    st.caption("Version 1.0")

# --------------------------------------------------
# End of Dashboard
# --------------------------------------------------