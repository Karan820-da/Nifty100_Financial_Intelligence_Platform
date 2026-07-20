import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import (
    get_base_data,
    get_company_list
)
st.title("📊 Peer Comparison")

st.write(
    "Compare a company with its peers using key financial metrics."
)

st.divider()

df = get_base_data()
companies = get_company_list()

selected_company = st.selectbox(
    "Select Company",
    companies
)
selected_row = df[df["company_id"] == selected_company].iloc[0]

sector = selected_row["broad_sector"]

peer_df = df[
    df["broad_sector"] == sector
].copy()

st.subheader(f"Peer Group - {sector}")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Companies", len(peer_df))

with col2:
    st.metric(
        "Average ROE",
        f"{peer_df['return_on_equity_pct'].mean():.2f}%"
    )

with col3:
    st.metric(
        "Average P/E",
        f"{peer_df['pe_ratio'].mean():.2f}"
    )

with col4:
    st.metric(
        "Average Quality",
        f"{peer_df['composite_quality_score'].mean():.1f}"
    )

st.subheader("ROE Comparison")

fig = px.bar(
    peer_df,
    x="company_id",
    y="return_on_equity_pct",
    color="company_id"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Peer Comparison Table")

columns = [
    "company_id",
    "broad_sector",
    "market_cap_crore",
    "pe_ratio",
    "return_on_equity_pct",
    "debt_to_equity",
    "composite_quality_score"
]

st.dataframe(
    peer_df[columns],
    use_container_width=True,
    hide_index=True
)