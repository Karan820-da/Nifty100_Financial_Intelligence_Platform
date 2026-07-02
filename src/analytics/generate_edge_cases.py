import pandas as pd
from sqlalchemy import create_engine

import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("mysql_user")
password = os.getenv("mysql_password")
host = os.getenv("mysql_host")
port = os.getenv("mysql_port")
database = os.getenv("mysql_database")

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)

print("loading financial ratio data...")

df = pd.read_sql(
    """
    select
        company_id,
        year,
        return_on_equity_pct,
        debt_to_equity
    from financial_ratios
    """,
    engine
)

edge_cases = []

for _, row in df.iterrows():

    roe = row["return_on_equity_pct"]
    de = row["debt_to_equity"]

    if pd.notna(roe) and abs(roe) > 1000:
        edge_cases.append(
            f"{row['company_id']} | {row['year']} | "
            f"abnormal roe = {roe} | "
            f"category = formula discrepancy"
        )

    if pd.notna(de) and de > 5:
        edge_cases.append(
            f"{row['company_id']} | {row['year']} | "
            f"high debt to equity = {de} | "
            f"category = review required"
        )


with open(
        "output/ratio_edge_cases.log",
        "w",
        encoding="utf-8"
) as file:

    for item in edge_cases:
        file.write(item + "\n")


print(
    f"{len(edge_cases)} anomalies written "
    "to output/ratio_edge_cases.log"
)