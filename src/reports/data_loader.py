"""
data_loader.py

Loads financial data from the MySQL database for the PDF Tearsheet.
"""

import pandas as pd

from src.dashboard.utils.db import get_engine

# Create database engine
engine = get_engine()


def load_company(company_id):
    """
    Load company master information.
    Example: company_id = "TCS"
    """

    query = f"""
    SELECT *
    FROM companies
    WHERE id = '{company_id}'
    """

    return pd.read_sql(query, engine)


def load_profit_loss(company_id):
    """
    Load Profit & Loss history.
    """

    query = f"""
    SELECT *
    FROM profitandloss
    WHERE company_id = '{company_id}'
    ORDER BY year
    """

    return pd.read_sql(query, engine)


def load_ratios(company_id):
    """
    Load financial ratios.
    """

    query = f"""
    SELECT *
    FROM financial_ratios
    WHERE company_id = '{company_id}'
    ORDER BY year
    """

    return pd.read_sql(query, engine)


def load_balance_sheet(company_id):
    """
    Load Balance Sheet history.
    """

    query = f"""
    SELECT *
    FROM balancesheet
    WHERE company_id = '{company_id}'
    ORDER BY year
    """

    return pd.read_sql(query, engine)


def load_cash_flow(company_id):
    """
    Load Cash Flow history.
    """

    query = f"""
    SELECT *
    FROM cashflow
    WHERE company_id = '{company_id}'
    ORDER BY year
    """

    return pd.read_sql(query, engine)


def load_market_cap(company_id):
    """
    Load Market Cap information.
    """

    query = f"""
    SELECT *
    FROM market_cap
    WHERE company_id = '{company_id}'
    """

    return pd.read_sql(query, engine)


def load_analysis(company_id):
    """
    Load AI / Fundamental analysis.
    """

    query = f"""
    SELECT *
    FROM analysis
    WHERE company_id = '{company_id}'
    """

    return pd.read_sql(query, engine)

def load_market_cap(company_id):
    """
    Load market cap and valuation metrics.
    """

    query = f"""
    SELECT *
    FROM market_cap
    WHERE company_id = '{company_id}'
    ORDER BY year DESC
    LIMIT 1
    """

    return pd.read_sql(query, engine)