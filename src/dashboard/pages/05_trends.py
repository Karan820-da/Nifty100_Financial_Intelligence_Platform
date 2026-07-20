import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import get_base_data

st.title("📈 Market Trends")

st.write(
    "Analyze historical trends across the Nifty100 companies."
)

st.divider()

df = get_base_data()

metric = st.selectbox(
    "Select Metric",
    [
        "return_on_equity_pct",
        "pe_ratio",
        "market_cap_crore",
        "composite_quality_score"
    ]
)
trend_df = (
    df.groupby("year")[metric]
    .mean()
    .reset_index()
)

fig = px.line(
    trend_df,
    x="year",
    y=metric,
    markers=True,
    title=f"Average {metric} Over Time"
)

st.plotly_chart(fig, use_container_width=True)

latest_year = df["year"].max()

latest_df = df[df["year"] == latest_year]

st.subheader(f"🏆 Top Companies ({latest_year})")

top10 = latest_df.nlargest(10, metric)

fig = px.bar(
    top10,
    x="company_id",
    y=metric,
    color="broad_sector"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("📋 Historical Data")

st.dataframe(
    trend_df,
    use_container_width=True,
    hide_index=True
)

metric_options = {
    "Return on Equity": "return_on_equity_pct",
    "P/E Ratio": "pe_ratio",
    "Market Cap": "market_cap_crore",
    "Quality Score": "composite_quality_score"
}

selected_metric = st.selectbox(
    "Select Metric",
    list(metric_options.keys())
)

metric = metric_options[selected_metric]