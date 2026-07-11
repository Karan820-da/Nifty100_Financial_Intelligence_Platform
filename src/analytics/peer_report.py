import os
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

# Create MySQL connection
engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)

query = """
select

    fr.company_id,
    fr.year,

    c.company_name,

    pg.peer_group_name,

    fr.return_on_equity_pct,
    c.roce_percentage,
    fr.net_profit_margin_pct,
    fr.debt_to_equity,
    fr.free_cash_flow_cr,
    fr.revenue_cagr_5yr,
    fr.pat_cagr_5yr,
    fr.eps_cagr_5yr,
    fr.composite_quality_score

from financial_ratios fr

left join companies c
    on fr.company_id = c.id

left join peer_groups pg
    on fr.company_id = pg.company_id
"""
df = pd.read_sql(
    query,
    engine
)

# Remove non-standard periods
df = df[
    ~df["year"].isin(
        [
            "TTM",
            "Mar 2016 9m",
            "Mar 2023 15"
        ]
    )
].copy()

# Convert year to datetime
df["year_dt"] = pd.to_datetime(
    df["year"],
    format="%b %Y",
    errors="coerce"
)

# Remove invalid dates
df = df.dropna(subset=["year_dt"])

# Keep latest record for each company
df = (
    df.sort_values("year_dt")
      .groupby("company_id")
      .tail(1)
      .reset_index(drop=True)
)

print("\nLatest Company Records")
print("=" * 50)

print(df.head(10))

print()

print("Total Companies :", len(df))

import os

os.makedirs(
    "output",
    exist_ok=True
)

output_file = "output/peer_comparison.xlsx"

with pd.ExcelWriter(
    output_file,
    engine="openpyxl"
) as writer:

    peer_groups = sorted(
        df["peer_group_name"]
        .dropna()
        .unique()
    )

    print()

    print("Generating Excel Report...\n")

    for group in peer_groups:

        group_df = (
            df[
                df["peer_group_name"] == group
            ]
            .sort_values(
                "composite_quality_score",
                ascending=False
            )
        )

        sheet_name = group[:31]

        group_df.to_excel(
            writer,
            sheet_name=sheet_name,
            index=False
        )

        print(
            f"{group} : {len(group_df)} companies exported."
        )

print()

print("=" * 60)
print("Peer Comparison Report Created Successfully")
print("=" * 60)
print(f"Saved to : {output_file}")