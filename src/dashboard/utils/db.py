# ==========================================================
# db.py
# Database Connection
# ==========================================================

import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine

# ----------------------------------------------------------
# Load Environment Variables
# ----------------------------------------------------------

load_dotenv()

# ----------------------------------------------------------
# Database Credentials
# ----------------------------------------------------------

MYSQL_USER = os.getenv("mysql_user")
MYSQL_PASSWORD = os.getenv("mysql_password")
MYSQL_HOST = os.getenv("mysql_host")
MYSQL_PORT = os.getenv("mysql_port")
MYSQL_DATABASE = os.getenv("mysql_database")


# ----------------------------------------------------------
# Database Engine
# ----------------------------------------------------------

@st.cache_resource
def get_engine():
    """
    Create and return the SQLAlchemy engine.
    """

    connection_string = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    )

    engine = create_engine(connection_string)

    return engine

# ==========================================================
# Base Data
# ==========================================================

@st.cache_data(ttl=600)
def get_base_data():
    """
    Returns a cleaned dataframe after joining all tables.
    """

    query = """
    SELECT

        fr.company_id,
        fr.year,

        s.broad_sector,
        s.sub_sector,
        s.index_weight_pct,
        s.market_cap_category,

        mc.market_cap_crore,
        mc.enterprise_value_crore,
        mc.pe_ratio,
        mc.pb_ratio,
        mc.ev_ebitda,
        mc.dividend_yield_pct,

        fr.net_profit_margin_pct,
        fr.operating_profit_margin_pct,
        fr.return_on_equity_pct,
        fr.debt_to_equity,
        fr.interest_coverage,
        fr.asset_turnover,
        fr.free_cash_flow_cr,
        fr.capex_cr,
        fr.earnings_per_share,
        fr.book_value_per_share,
        fr.dividend_payout_ratio_pct,
        fr.total_debt_cr,
        fr.cash_from_operations_cr,
        fr.revenue_cagr_5yr,
        fr.pat_cagr_5yr,
        fr.eps_cagr_5yr,
        fr.composite_quality_score

    FROM financial_ratios fr

    LEFT JOIN market_cap mc
        ON fr.company_id = mc.company_id
        AND RIGHT(fr.year,4) = CAST(mc.year AS CHAR)

    LEFT JOIN sectors s
        ON fr.company_id = s.company_id
    """

    engine = get_engine()

    df = pd.read_sql(query, engine)
    # ----------------------------------------------------------
    # Remove Duplicate Records
    # ----------------------------------------------------------

    df = df.drop_duplicates()

    # ----------------------------------------------------------
    # Convert Numeric Columns
    # ----------------------------------------------------------

    numeric_columns = [
        "index_weight_pct",
        "market_cap_crore",
        "enterprise_value_crore",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "dividend_yield_pct",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "return_on_equity_pct",
        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",
        "free_cash_flow_cr",
        "capex_cr",
        "earnings_per_share",
        "book_value_per_share",
        "dividend_payout_ratio_pct",
        "total_debt_cr",
        "cash_from_operations_cr",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr",
        "composite_quality_score"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # ----------------------------------------------------------
    # Clean Text Columns
    # ----------------------------------------------------------

    text_columns = [
        "company_id",
        "year",
        "broad_sector",
        "sub_sector",
        "market_cap_category"
    ]

    for column in text_columns:
        df[column] = df[column].astype(str).str.strip()

    # ----------------------------------------------------------
    # Sort Data
    # ----------------------------------------------------------

    df = (
        df.sort_values(
            by=["company_id", "year"]
        )
        .reset_index(drop=True)
    )

    return df

# ==========================================================
# Home Page Data
# ==========================================================

@st.cache_data(ttl=600)
def get_home_data():
    """
    Returns the complete dataset for the Home Dashboard.
    """

    df = get_base_data()

    return df

# ==========================================================
# Company Profile Data
# ==========================================================

@st.cache_data(ttl=600)
def get_company_profile(company_id):
    """
    Returns data for a selected company.
    """

    df = get_base_data()

    company_df = df[df["company_id"] == company_id].copy()

    return company_df

# ==========================================================
# Company List
# ==========================================================

@st.cache_data(ttl=600)
def get_company_list():
    """
    Returns a sorted list of all available companies.
    """

    df = get_base_data()

    companies = sorted(df["company_id"].unique())

    return companies

# ==========================================================
# Sector Data
# ==========================================================

@st.cache_data(ttl=600)
def get_sector_data(sector):
    """
    Returns data for a selected sector.
    """

    df = get_base_data()

    sector_df = df[df["broad_sector"] == sector].copy()

    return sector_df

# ==========================================================
# Market Summary
# ==========================================================

@st.cache_data(ttl=600)
def get_market_summary():
    """
    Returns summary statistics for the Home Dashboard.
    """

    df = get_base_data()

    summary = {
        "total_companies": df["company_id"].nunique(),
        "total_sectors": df["broad_sector"].nunique(),
        "average_pe": round(df["pe_ratio"].mean(), 2),
        "average_roe": round(df["return_on_equity_pct"].mean(), 2),
        "total_market_cap": round(df["market_cap_crore"].sum(), 2)
    }

    return summary

# ==========================================================
# Top Companies
# ==========================================================

@st.cache_data(ttl=600)
def get_top_companies(metric, top_n=10):
    """
    Returns the top companies based on a selected metric.
    """

    df = get_base_data()

    top_companies = (
        df.sort_values(by=metric, ascending=False)
          .head(top_n)
          .copy()
    )

    return top_companies

# ==========================================================
# Year List
# ==========================================================

@st.cache_data(ttl=600)
def get_year_list():
    """
    Returns a sorted list of all available years.
    """

    df = get_base_data()

    years = (
        df["year"]
        .dropna()
        .unique()
        .tolist()
    )

    years.sort()

    return years

# ==========================================================
# Sector List
# ==========================================================

@st.cache_data(ttl=600)
def get_sector_list():
    """
    Returns a sorted list of all available sectors.
    """

    df = get_base_data()

    sectors = (
        df["broad_sector"]
        .dropna()
        .unique()
        .tolist()
    )

    sectors.sort()

    return sectors

# ==========================================================
# Filter Options
# ==========================================================

@st.cache_data(ttl=600)
def get_filter_options():
    """
    Returns all filter options used across the dashboard.
    """

    filters = {
        "companies": get_company_list(),
        "years": get_year_list(),
        "sectors": get_sector_list()
    }

    return filters

# ==========================================================
# Refresh Cached Data
# ==========================================================

def refresh_data():
    """
    Clears all cached data and resources.
    """

    st.cache_data.clear()
    st.cache_resource.clear()