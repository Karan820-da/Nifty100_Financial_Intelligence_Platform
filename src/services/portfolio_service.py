from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

CSV_PATH = BASE_DIR / "output" / "portfolio_stats.csv"


def get_portfolio_stats():

    df = pd.read_csv(CSV_PATH)

    df.columns = [
        "kpi",
        "p10",
        "p25",
        "p50",
        "p75",
        "p90",
        "mean",
        "std"
    ]

    return df.to_dict(orient="records")
