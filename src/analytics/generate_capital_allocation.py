import pandas as pd
from sqlalchemy import create_engine

from cashflow_kpis import (
    capital_allocation_pattern
)
# MySQL Connection
username = "root"
password = "**********"
host = "localhost"
port = "3306"
database = "nifty100_db"

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)

print("Loading cashflow data...")

df = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        operating_activity,
        investing_activity,
        financing_activity
    FROM cashflow
    """,
    engine
)

print(f"{len(df)} rows loaded.")


df["cfo_sign"] = df["operating_activity"].apply(
    lambda x: "+" if x >= 0 else "-"
)

df["cfi_sign"] = df["investing_activity"].apply(
    lambda x: "+" if x >= 0 else "-"
)

df["cff_sign"] = df["financing_activity"].apply(
    lambda x: "+" if x >= 0 else "-"
)


df["pattern_label"] = df.apply(
    lambda row:
    capital_allocation_pattern(
        row["operating_activity"],
        row["investing_activity"],
        row["financing_activity"]
    ),
    axis=1
)


output_file = "output/capital_allocation.csv"

df.to_csv(
    output_file,
    index=False
)

print(
    f"Capital allocation file saved: {output_file}"
)