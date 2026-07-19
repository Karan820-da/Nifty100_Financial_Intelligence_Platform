import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.db import get_peer_data

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Peer Comparison",
    page_icon="🤝",
    layout="wide"
)

st.title("🤝 Peer Comparison")

st.caption(
    "Compare multiple companies using key financial metrics."
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------

df = get_peer_data()

if df.empty:
    st.error("No company data available.")
    st.stop()

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.header("Comparison")

companies = sorted(df["company_id"].unique())

base_company = st.sidebar.selectbox(
    "Base Company",
    companies
)

available_peers = [
    c for c in companies
    if c != base_company
]

peer_companies = st.sidebar.multiselect(
    "Select Peer Companies",
    available_peers,
    max_selections=5
)

selected_companies = [base_company] + peer_companies

compare_df = df[
    df["company_id"].isin(selected_companies)
].copy()

if compare_df.empty:
    st.warning("Select companies to compare.")
    st.stop()

st.markdown("### Selected Companies")

st.write(
    " | ".join(selected_companies)
)

st.markdown("---")

# --------------------------------------------------
# Company KPI Comparison
# --------------------------------------------------

st.subheader("📊 Financial Comparison")

# Create one column for each selected company
cols = st.columns(len(compare_df))

for col, (_, company) in zip(cols, compare_df.iterrows()):

    with col:

        # Highlight the base company
        if company["company_id"] == base_company:
            st.success(f"### 🏢 {company['company_id']}")
        else:
            st.info(f"### {company['company_id']}")

        st.metric(
            "💰 Market Cap",
            f"₹ {company['market_cap_crore']:,.0f} Cr"
            if pd.notna(company["market_cap_crore"])
            else "N/A"
        )

        st.metric(
            "📈 PE Ratio",
            f"{company['pe_ratio']:.2f}"
            if pd.notna(company["pe_ratio"])
            else "N/A"
        )

        st.metric(
            "📚 PB Ratio",
            f"{company['pb_ratio']:.2f}"
            if pd.notna(company["pb_ratio"])
            else "N/A"
        )

        st.metric(
            "📊 ROE",
            f"{company['return_on_equity_pct']:.2f}%"
            if pd.notna(company["return_on_equity_pct"])
            else "N/A"
        )

        st.metric(
            "🏦 Debt / Equity",
            f"{company['debt_to_equity']:.2f}"
            if pd.notna(company["debt_to_equity"])
            else "N/A"
        )

        st.metric(
            "⭐ Quality Score",
            f"{company['composite_quality_score']:.2f}"
            if pd.notna(company["composite_quality_score"])
            else "N/A"
        )

st.markdown("---")
# --------------------------------------------------
# Radar Chart Comparison
# --------------------------------------------------

st.subheader("🕸️ Multi-Factor Company Comparison")

radar_df = compare_df.copy()

# Normalize metrics to a 0–100 scale
metrics = [
    "return_on_equity_pct",
    "revenue_cagr_5yr",
    "composite_quality_score",
    "pe_ratio",
    "debt_to_equity"
]

for metric in metrics:

    max_val = radar_df[metric].max()
    min_val = radar_df[metric].min()

    if pd.isna(max_val) or max_val == min_val:
        radar_df[f"{metric}_norm"] = 100

    else:

        radar_df[f"{metric}_norm"] = (
            (radar_df[metric] - min_val)
            /
            (max_val - min_val)
        ) * 100

# Lower PE is better
radar_df["pe_ratio_norm"] = 100 - radar_df["pe_ratio_norm"]

# Lower Debt is better
radar_df["debt_to_equity_norm"] = 100 - radar_df["debt_to_equity_norm"]

categories = [
    "ROE",
    "Revenue CAGR",
    "Quality",
    "PE",
    "Debt"
]

fig = go.Figure()

for _, row in radar_df.iterrows():

    values = [

        row["return_on_equity_pct_norm"],

        row["revenue_cagr_5yr_norm"],

        row["composite_quality_score_norm"],

        row["pe_ratio_norm"],

        row["debt_to_equity_norm"]

    ]

    values += values[:1]

    fig.add_trace(

        go.Scatterpolar(

            r=values,

            theta=categories + [categories[0]],

            fill="toself",

            name=row["company_id"]

        )

    )

fig.update_layout(

    polar=dict(

        radialaxis=dict(

            visible=True,

            range=[0, 100]

        )

    ),

    height=600,

    showlegend=True,

    title="Financial Strength Comparison"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

# --------------------------------------------------
# Grouped Comparison Charts
# --------------------------------------------------

st.subheader("📊 Metric Comparison")

chart_col1, chart_col2 = st.columns(2)

# Market Cap

fig_marketcap = px.bar(

    compare_df,

    x="company_id",

    y="market_cap_crore",

    color="company_id",

    text_auto=".2s",

    title="Market Capitalization"

)

fig_marketcap.update_layout(height=450)

with chart_col1:

    st.plotly_chart(

        fig_marketcap,

        use_container_width=True

    )

# ROE

fig_roe = px.bar(

    compare_df,

    x="company_id",

    y="return_on_equity_pct",

    color="company_id",

    text_auto=".2f",

    title="Return on Equity"

)

fig_roe.update_layout(height=450)

with chart_col2:

    st.plotly_chart(

        fig_roe,

        use_container_width=True

    )

# --------------------------------------------------
# Second Row
# --------------------------------------------------

chart_col3, chart_col4 = st.columns(2)

# PE Ratio

fig_pe = px.bar(

    compare_df,

    x="company_id",

    y="pe_ratio",

    color="company_id",

    text_auto=".2f",

    title="PE Ratio"

)

fig_pe.update_layout(height=450)

with chart_col3:

    st.plotly_chart(

        fig_pe,

        use_container_width=True

    )

# Quality Score

fig_quality = px.bar(

    compare_df,

    x="company_id",

    y="composite_quality_score",

    color="company_id",

    text_auto=".2f",

    title="Quality Score"

)

fig_quality.update_layout(height=450)

with chart_col4:

    st.plotly_chart(

        fig_quality,

        use_container_width=True

    )

st.markdown("---")

# --------------------------------------------------
# Detailed Comparison Table
# --------------------------------------------------

st.subheader("📋 Detailed Financial Comparison")

comparison_table = compare_df[
    [
        "company_id",
        "broad_sector",
        "market_cap_category",
        "market_cap_crore",
        "enterprise_value_crore",
        "pe_ratio",
        "pb_ratio",
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "free_cash_flow_cr",
        "earnings_per_share",
        "book_value_per_share",
        "dividend_yield_pct",
        "composite_quality_score"
    ]
].copy()

comparison_table.columns = [
    "Company",
    "Sector",
    "Market Cap Category",
    "Market Cap (₹ Cr)",
    "Enterprise Value (₹ Cr)",
    "PE",
    "PB",
    "ROE (%)",
    "Debt/Equity",
    "Revenue CAGR (%)",
    "Free Cash Flow (₹ Cr)",
    "EPS",
    "Book Value",
    "Dividend Yield (%)",
    "Quality Score"
]

st.dataframe(
    comparison_table,
    use_container_width=True,
    hide_index=True,
    height=500
)

st.markdown("---")

# --------------------------------------------------
# Winner Analysis
# --------------------------------------------------

st.subheader("🏆 Overall Winner")

winner_df = compare_df.copy()

score_columns = [
    "return_on_equity_pct",
    "revenue_cagr_5yr",
    "composite_quality_score",
    "debt_to_equity"
]

for col in score_columns:
    winner_df[col] = winner_df[col].fillna(0)

# Normalize metrics
winner_df["roe_score"] = (
    winner_df["return_on_equity_pct"] /
    winner_df["return_on_equity_pct"].max()
)

winner_df["growth_score"] = (
    winner_df["revenue_cagr_5yr"] /
    winner_df["revenue_cagr_5yr"].max()
)

winner_df["quality_score"] = (
    winner_df["composite_quality_score"] /
    winner_df["composite_quality_score"].max()
)

max_debt = winner_df["debt_to_equity"].max()

if max_debt == 0:
    winner_df["debt_score"] = 1
else:
    winner_df["debt_score"] = (
        1 -
        (winner_df["debt_to_equity"] / max_debt)
    )

winner_df["overall_score"] = (

    winner_df["quality_score"] * 0.40 +

    winner_df["roe_score"] * 0.30 +

    winner_df["growth_score"] * 0.20 +

    winner_df["debt_score"] * 0.10

) * 100

winner_df = winner_df.sort_values(
    "overall_score",
    ascending=False
)

winner = winner_df.iloc[0]

st.success(f"""
## 🥇 {winner['company_id']}

### Overall Score: **{winner['overall_score']:.2f}/100**

**Sector:** {winner['broad_sector']}

**ROE:** {winner['return_on_equity_pct']:.2f}%

**Revenue CAGR:** {winner['revenue_cagr_5yr']:.2f}%

**Quality Score:** {winner['composite_quality_score']:.2f}

This company achieved the highest weighted score among the selected companies.
""")

st.markdown("---")

# --------------------------------------------------
# Download Comparison
# --------------------------------------------------

csv = comparison_table.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Comparison Report",
    csv,
    "peer_comparison.csv",
    "text/csv"
)

# --------------------------------------------------
# Styling
# --------------------------------------------------

st.markdown("""
<style>

div[data-testid="metric-container"]{
    background:#f8f9fa;
    border-radius:12px;
    padding:15px;
    border:1px solid #dddddd;
}

.block-container{
    padding-top:2rem;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Nifty100 Financial Intelligence Platform | Peer Comparison Dashboard"
)