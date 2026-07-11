import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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


def load_data():

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
        fr.pat_cagr_5yr,
        fr.revenue_cagr_5yr,
        fr.composite_quality_score

    from financial_ratios fr

    left join companies c
        on fr.company_id = c.id

    left join peer_groups pg
        on fr.company_id = pg.company_id
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

    df = df.dropna(subset=["year_dt"])

    # Keep latest financial year
    df = (
        df.sort_values("year_dt")
          .groupby("company_id")
          .tail(1)
          .reset_index(drop=True)
    )

    return df




def create_radar_chart(df, company_id):

    metrics = [
        "return_on_equity_pct",
        "roce_percentage",
        "net_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "pat_cagr_5yr",
        "revenue_cagr_5yr",
        "composite_quality_score"
    ]

    company = df[df["company_id"] == company_id]

    if company.empty:
        print(f"{company_id} not found.")
        return

    peer_group = company.iloc[0]["peer_group_name"]

    peers = df[df["peer_group_name"] == peer_group]

    company_values = company[metrics].iloc[0].fillna(0).tolist()

    peer_values = peers[metrics].mean().fillna(0).tolist()

    labels = [
        "ROE",
        "ROCE",
        "NPM",
        "D/E",
        "FCF",
        "PAT CAGR",
        "Revenue CAGR",
        "Quality Score"
    ]

    angles = np.linspace(
        0,
        2 * np.pi,
        len(labels),
        endpoint=False
    ).tolist()

    company_values += company_values[:1]
    peer_values += peer_values[:1]
    angles += angles[:1]

    plt.figure(figsize=(8, 8))

    ax = plt.subplot(111, polar=True)

    ax.plot(
        angles,
        company_values,
        linewidth=2,
        label=company_id
    )

    ax.fill(
        angles,
        company_values,
        alpha=0.25
    )

    ax.plot(
        angles,
        peer_values,
        linestyle="--",
        linewidth=2,
        label="Peer Average"
    )

    ax.set_xticks(angles[:-1])

    ax.set_xticklabels(labels)

    plt.title(
        f"{company.iloc[0]['company_name']}\n{peer_group}"
    )

    plt.legend(
        loc="upper right"
    )

    os.makedirs(
        "reports/radar_charts",
        exist_ok=True
    )

    plt.savefig(
        f"reports/radar_charts/{company_id}_radar.png"
    )

    plt.close()

    print(f"{company_id} chart created.")

if __name__ == "__main__":

    df = load_data()

    print("\nGenerating radar charts...\n")

    for company in df["company_id"]:

        create_radar_chart(
            df,
            company
        )

    print("\n======================================")
    print("Radar charts generated successfully.")
    print(f"Total Charts : {len(df)}")
    print("Location : reports/radar_charts/")
    print("======================================")