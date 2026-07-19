import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import get_trend_data

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="Trends Analysis",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Financial Trends Analysis")

st.markdown(
    """
Analyze the historical financial performance of a company across multiple years.
"""
)

# -------------------------------------------------------
# Load Data
# -------------------------------------------------------

df = get_trend_data()

# -------------------------------------------------------
# Company Selection
# -------------------------------------------------------

companies = sorted(df["company_id"].dropna().unique())

selected_company = st.selectbox(
    "Select Company",
    companies
)

# -------------------------------------------------------
# Metric Selection
# -------------------------------------------------------

metric_options = {
    "Return on Equity (%)": "return_on_equity_pct",
    "P/E Ratio": "pe_ratio",
    "Revenue CAGR (%)": "revenue_cagr_5yr",
    "Debt to Equity": "debt_to_equity",
    "Quality Score": "composite_quality_score"
}

metric_name = st.selectbox(
    "Select Financial Metric",
    list(metric_options.keys())
)

selected_metric = metric_options[metric_name]

# -------------------------------------------------------
# Filter Data
# -------------------------------------------------------

trend_df = (
    df[df["company_id"] == selected_company]
    .sort_values("year_dt")
    .copy()
)

trend_df = trend_df.dropna(
    subset=[selected_metric]
)

if trend_df.empty:
    st.warning("No historical data available.")
    st.stop()

# -------------------------------------------------------
# KPI Cards
# -------------------------------------------------------

latest_value = trend_df[selected_metric].iloc[-1]
highest_value = trend_df[selected_metric].max()
lowest_value = trend_df[selected_metric].min()
average_value = trend_df[selected_metric].mean()

if len(trend_df) > 1:

    first_value = trend_df[selected_metric].iloc[0]

    if pd.notna(first_value) and first_value != 0:

        growth = (
            (latest_value - first_value)
            / abs(first_value)
        ) * 100

    else:
        growth = 0

else:

    growth = 0

st.markdown("---")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Latest",
    f"{latest_value:.2f}"
)

col2.metric(
    "Highest",
    f"{highest_value:.2f}"
)

col3.metric(
    "Lowest",
    f"{lowest_value:.2f}"
)

col4.metric(
    "Average",
    f"{average_value:.2f}"
)

col5.metric(
    "Growth %",
    f"{growth:.2f}%"
)

# -------------------------------------------------------
# Moving Average
# -------------------------------------------------------

trend_df["Moving Average"] = (
    trend_df[selected_metric]
    .rolling(window=2)
    .mean()
)

# -------------------------------------------------------
# Trend Chart
# -------------------------------------------------------

st.markdown("---")

st.subheader(f"📈 {metric_name} Trend")

fig = px.line(
    trend_df,
    x="year_dt",
    y=selected_metric,
    markers=True,
    title=f"{selected_company} - {metric_name}"
)

# Actual values
fig.update_traces(
    line=dict(width=3),
    marker=dict(size=8),
    name=metric_name
)

# Moving Average
fig.add_scatter(
    x=trend_df["year_dt"],
    y=trend_df["Moving Average"],
    mode="lines",
    name="Moving Average"
)

fig.update_layout(
    template="plotly_white",
    hovermode="x unified",
    xaxis_title="Year",
    yaxis_title=metric_name,
    height=550,
    legend_title="Metrics"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------------
# Historical Data
# -------------------------------------------------------

st.markdown("---")

st.subheader("📋 Historical Data")

history = trend_df[
    [
        "year",
        selected_metric
    ]
].rename(
    columns={
        "year": "Year",
        selected_metric: metric_name
    }
)

st.dataframe(
    history,
    use_container_width=True,
    hide_index=True
)

# -------------------------------------------------------
# Summary Statistics
# -------------------------------------------------------

st.markdown("---")

st.subheader("📊 Summary Statistics")

summary = history.describe().T

st.dataframe(
    summary,
    use_container_width=True
)

# -------------------------------------------------------
# Download CSV
# -------------------------------------------------------

st.markdown("---")

csv = history.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Historical Data",
    data=csv,
    file_name=f"{selected_company}_trend_history.csv",
    mime="text/csv"
)