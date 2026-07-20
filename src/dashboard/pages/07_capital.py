import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import get_base_data

st.title("💰 Market Capitalization")

st.write(
    "Analyze market capitalization across Nifty100 companies."
)

st.divider()

df = get_base_data()

capital_df = (
    df.sort_values("year")
      .drop_duplicates(subset="company_id", keep="last")
)

st.subheader("📊 Market Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Market Cap",
        f"₹{capital_df['market_cap_crore'].sum():,.0f} Cr"
    )

with col2:
    largest = capital_df.loc[
        capital_df["market_cap_crore"].idxmax()
    ]
    st.metric(
        "Largest Company",
        largest["company_id"]
    )

with col3:
    st.metric(
        "Average Market Cap",
        f"₹{capital_df['market_cap_crore'].mean():,.0f} Cr"
    )

with col4:
    st.metric(
        "Companies",
        capital_df["company_id"].nunique()
    )

st.subheader("🏆 Top 10 Companies")

top10 = capital_df.nlargest(
    10,
    "market_cap_crore"
)

fig = px.bar(
    top10,
    x="company_id",
    y="market_cap_crore",
    color="company_id"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📊 Market Cap Distribution")

fig = px.histogram(
    capital_df,
    x="market_cap_crore",
    nbins=20
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🥧 Market Cap by Sector")

sector_cap = (
    capital_df
    .groupby("broad_sector")["market_cap_crore"]
    .sum()
    .reset_index()
)

fig = px.pie(
    sector_cap,
    names="broad_sector",
    values="market_cap_crore"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📋 Company Market Cap")

columns = [
    "company_id",
    "broad_sector",
    "market_cap_crore",
    "market_cap_category",
    "pe_ratio",
    "return_on_equity_pct"
]

st.dataframe(
    capital_df[columns],
    use_container_width=True,
    hide_index=True
)

