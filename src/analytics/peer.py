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

query = """
select

    fr.company_id,
    fr.year,

    pg.peer_group_name,

    fr.return_on_equity_pct,
    c.roce_percentage,
    fr.net_profit_margin_pct,
    fr.debt_to_equity,
    fr.free_cash_flow_cr,
    fr.revenue_cagr_5yr,
    fr.pat_cagr_5yr,
    fr.eps_cagr_5yr,
    fr.interest_coverage,
    fr.asset_turnover

from financial_ratios fr

left join peer_groups pg
    on fr.company_id = pg.company_id

left join companies c
    on fr.company_id = c.id
"""

df = pd.read_sql(query, engine)

metrics = [

    "return_on_equity_pct",
    "roce_percentage",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "eps_cagr_5yr",
    "interest_coverage",
    "asset_turnover"

]

records = []

for peer_name, peer_df in df.groupby("peer_group_name"):

    if pd.isna(peer_name):
        continue

    peer_df = peer_df.copy()

    for metric in metrics:

        if metric not in peer_df.columns:
            continue

        temp = peer_df[
            [
                "company_id",
                "year",
                "peer_group_name",
                metric
            ]
        ].copy()

        temp = temp.dropna(subset=[metric])

        if len(temp) == 0:
            continue

        temp["percentile_rank"] = (
            temp[metric]
            .rank(
                pct=True,
                method="average"
            )
            * 100
        )

        if metric == "debt_to_equity":

            temp["percentile_rank"] = (
                100 - temp["percentile_rank"]
            )

        temp.rename(
            columns={
                metric: "metric_value"
            },
            inplace=True
        )

        temp["metric"] = metric

        records.append(temp)

result = pd.concat(
    records,
    ignore_index=True
)

result = result[
    [
        "company_id",
        "peer_group_name",
        "metric",
        "metric_value",
        "percentile_rank",
        "year"
    ]
]

result.to_sql(

    "peer_percentiles",

    engine,

    if_exists="replace",

    index=False

)

print()

print("=" * 50)
print("Peer Percentile Ranking Completed")
print("=" * 50)

print()

print("Rows inserted :", len(result))

print()

print(result.head(20))