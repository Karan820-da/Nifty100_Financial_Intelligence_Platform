import os
import pandas as pd
from sqlalchemy import create_engine
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


def calculate_cagr(beginning, ending, years):

    if (
        pd.isna(beginning)
        or pd.isna(ending)
        or beginning <= 0
        or ending <= 0
        or years <= 0
    ):
        return None

    return round(
        (((ending / beginning) ** (1 / years)) - 1) * 100,
        2
    )


query = """
select
    company_id,
    year,
    sales,
    net_profit,
    eps
from profitandloss
"""

df = pd.read_sql(query, engine)

# Remove invalid periods
df = df[
    ~df["year"].isin(
        [
            "TTM",
            "Mar 2016 9m",
            "Mar 2023 15"
        ]
    )
].copy()

# Convert year
df["year_dt"] = pd.to_datetime(
    df["year"],
    format="%b %Y",
    errors="coerce"
)

# Drop invalid dates
df = df.dropna(subset=["year_dt"])

df = df.sort_values(
    ["company_id", "year_dt"]
)

updates = []

for company, group in df.groupby("company_id"):

    group = group.reset_index(drop=True)

    for i in range(5, len(group)):

        current = group.loc[i]
        previous = group.loc[i - 5]

        revenue_cagr = calculate_cagr(
            previous["sales"],
            current["sales"],
            5
        )

        pat_cagr = calculate_cagr(
            previous["net_profit"],
            current["net_profit"],
            5
        )

        eps_cagr = calculate_cagr(
            previous["eps"],
            current["eps"],
            5
        )

        updates.append(
            [
                revenue_cagr,
                pat_cagr,
                eps_cagr,
                company,
                current["year"]
            ]
        )

update_df = pd.DataFrame(
    updates,
    columns=[
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr",
        "company_id",
        "year"
    ]
)

# Convert NaN to None
update_df = update_df.astype(object)
update_df = update_df.where(
    pd.notnull(update_df),
    None
)

print("\nSample Output:")
print(update_df.head())

print("\nRows with Missing CAGR:")
print(
    update_df[
        update_df.isnull().any(axis=1)
    ]
)

connection = engine.raw_connection()
cursor = connection.cursor()

sql = """
update financial_ratios
set
    revenue_cagr_5yr=%s,
    pat_cagr_5yr=%s,
    eps_cagr_5yr=%s
where
    company_id=%s
and
    year=%s
"""

cursor.executemany(
    sql,
    update_df.values.tolist()
)

connection.commit()

print(f"\nUpdated {cursor.rowcount} rows successfully.")

cursor.close()
connection.close()