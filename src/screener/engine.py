import os
import yaml
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

username = os.getenv("mysql_user")
password = os.getenv("mysql_password")
host = os.getenv("mysql_host")
port = os.getenv("mysql_port")
database = os.getenv("mysql_database")

# Database connection
engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)


def load_config():
    """Load screener configuration."""
    with open(
        "config/screener_config.yaml",
        "r"
    ) as file:
        return yaml.safe_load(file)


def load_financial_ratios():
    """Load latest financial data."""

    query = """
    select

        fr.*,

        p.sales,
        p.net_profit,
        p.eps,
        p.dividend_payout,

        mc.market_cap_crore,
        mc.pe_ratio,
        mc.pb_ratio,
        mc.dividend_yield_pct,

        c.company_name,
        c.roce_percentage

    from financial_ratios fr

    left join profitandloss p
        on fr.company_id = p.company_id
        and fr.year = p.year

    left join market_cap mc
        on fr.company_id = mc.company_id
        and fr.year = mc.year

    left join companies c
        on fr.company_id = c.id
    """

    df = pd.read_sql(query, engine)

    # Clean year values
    df["year"] = (
        df["year"]
        .astype(str)
        .str.replace(r"\s+\d+m$", "", regex=True)
        .str.replace(r"\s+\d+$", "", regex=True)
    )

    # Convert to datetime
    df["year_dt"] = pd.to_datetime(
        df["year"],
        format="%b %Y",
        errors="coerce"
    )

    # Remove invalid dates
    df = df.dropna(subset=["year_dt"])

    # Sort and keep latest record
    df = df.sort_values("year_dt")

    df = (
        df.groupby(
            "company_id",
            as_index=False
        )
        .tail(1)
    )

    return df


def apply_filters(df, filters):

    if "roe_min" in filters:
        df = df[
            df["return_on_equity_pct"] >= filters["roe_min"]
        ]

    if "debt_to_equity_max" in filters:
        df = df[
            df["debt_to_equity"] <= filters["debt_to_equity_max"]
        ]

    if "free_cash_flow_min" in filters:
        df = df[
            df["free_cash_flow_cr"] >= filters["free_cash_flow_min"]
        ]

    if "revenue_cagr_5yr_min" in filters:
        df = df[
            df["revenue_cagr_5yr"] >= filters["revenue_cagr_5yr_min"]
        ]

    if "pat_cagr_5yr_min" in filters:
        df = df[
            df["pat_cagr_5yr"] >= filters["pat_cagr_5yr_min"]
        ]

    if "sales_min" in filters:
        df = df[
            df["sales"] >= filters["sales_min"]
        ]

    if "pe_ratio_max" in filters:
        df = df[
            df["pe_ratio"] <= filters["pe_ratio_max"]
        ]

    if "pb_ratio_max" in filters:
        df = df[
            df["pb_ratio"] <= filters["pb_ratio_max"]
        ]

    if "dividend_yield_min" in filters:
        df = df[
            df["dividend_yield_pct"] >= filters["dividend_yield_min"]
        ]

    if "dividend_payout_max" in filters:
        df = df[
            df["dividend_payout"] <= filters["dividend_payout_max"]
        ]

    return df.sort_values(
        by="composite_quality_score",
        ascending=False
    )


def run_preset(preset_name):

    config = load_config()

    df = load_financial_ratios()

    result = apply_filters(
        df,
        config[preset_name]
    )

    print("\n" + "=" * 60)
    print(f"Preset : {preset_name}")
    print(f"Companies Found : {len(result)}")
    print("=" * 60)

    print(
        result[
            [
                "company_id",
                "company_name",
                "return_on_equity_pct",
                "debt_to_equity",
                "free_cash_flow_cr",
                "revenue_cagr_5yr",
                "pat_cagr_5yr",
                "market_cap_crore",
                "pe_ratio",
                "pb_ratio",
                "dividend_yield_pct",
                "composite_quality_score"
            ]
        ].head(10)
    )

    return result


if __name__ == "__main__":
    run_preset("quality_compounder")