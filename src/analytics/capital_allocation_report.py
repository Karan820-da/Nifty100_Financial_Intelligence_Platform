"""
Sprint 5 - Day 32
Capital Allocation Report
"""

import pandas as pd

from pathlib import Path

from src.dashboard.utils.db import get_engine
from src.analytics.cashflow_kpis import capital_allocation_pattern

engine = get_engine()

cashflow = pd.read_sql(
    "SELECT * FROM cashflow",
    engine
)

profit = pd.read_sql(
    "SELECT company_id,year,net_profit FROM profitandloss",
    engine
)

companies = pd.read_sql(
    """
    SELECT
        id AS company_id,
        company_name
    FROM companies
    """,
    engine
)

cashflow["company_id"] = cashflow["company_id"].str.strip()
companies["company_id"] = companies["company_id"].str.strip()

df = cashflow.merge(
    profit,
    on=["company_id","year"],
    how="left"
)

df = df.merge(
    companies,
    on="company_id",
    how="left"
)

df["company_name"] = (
    df["company_name"]
    .fillna(df["company_id"])
    .str.strip()
)

df["year_num"] = pd.to_numeric(
    df["year"].str.extract(r"(\d{4})")[0],
    errors="coerce"
)

df = df.dropna(subset=["year_num"])

df["year_num"] = df["year_num"].astype(int)

df = df.drop_duplicates(
    subset=["company_id","year"]
)

patterns = []

for company in sorted(df["company_id"].unique()):

    company_df = (
        df[df["company_id"] == company]
        .sort_values("year_num")
    )

    for _, row in company_df.iterrows():

        ratio = (
            row["operating_activity"] /
            row["net_profit"]
            if row["net_profit"] != 0
            else None
        )

        if ratio is None:
            quality = "Insufficient Data"
        elif ratio > 1:
            quality = "High Quality"
        elif ratio >= 0.5:
            quality = "Moderate"
        else:
            quality = "Accrual Risk"

        pattern = capital_allocation_pattern(
            row["operating_activity"],
            row["investing_activity"],
            row["financing_activity"],
            quality
        )

        patterns.append({

            "company_id": company,

            "company_name": row["company_name"],

            "year": row["year"],

            "year_num": row["year_num"],

            "capital_allocation": pattern

        })

patterns_df = pd.DataFrame(patterns)

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

patterns_df.to_csv(
    output_dir / "capital_allocation.csv",
    index=False
)

latest_year = patterns_df["year_num"].max()

latest = patterns_df[
    patterns_df["year_num"] == latest_year
]

distribution = (
    latest["capital_allocation"]
    .value_counts()
    .reset_index()
)

distribution.columns = [
    "Capital Allocation Pattern",
    "Companies"
]

print("\nLatest Year Distribution\n")

print(distribution)

distribution.to_csv(
    output_dir / "capital_allocation_distribution.csv",
    index=False
)

changes = []

for company in patterns_df["company_id"].unique():

    company_df = (
        patterns_df[
            patterns_df["company_id"] == company
        ]
        .sort_values("year_num")
    )

    if len(company_df) < 2:
        continue

    previous = company_df.iloc[-2]
    latest = company_df.iloc[-1]

    if previous["capital_allocation"] != latest["capital_allocation"]:

        changes.append({

            "company_id": company,

            "company_name": latest["company_name"],

            "previous_year": previous["year"],

            "latest_year": latest["year"],

            "previous_pattern":
                previous["capital_allocation"],

            "latest_pattern":
                latest["capital_allocation"]

        })

changes_df = pd.DataFrame(changes)

changes_df.to_csv(
    output_dir / "pattern_changes.csv",
    index=False
)