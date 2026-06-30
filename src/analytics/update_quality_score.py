import pandas as pd
from sqlalchemy import create_engine

username = "root"
password = "Kaikira820"
host = "localhost"
port = "3306"
database = "nifty100_db"

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)

query = """
select
id,
return_on_equity_pct,
net_profit_margin_pct,
asset_turnover
from financial_ratios
"""

df = pd.read_sql(query, engine)

df["return_on_equity_pct"] = df[
    "return_on_equity_pct"
].fillna(0)

df["net_profit_margin_pct"] = df[
    "net_profit_margin_pct"
].fillna(0)

df["asset_turnover"] = df[
    "asset_turnover"
].fillna(0)

df["composite_quality_score"] = (
    0.4 * df["return_on_equity_pct"]
    + 0.3 * df["net_profit_margin_pct"]
    + 0.3 * df["asset_turnover"]
).round(2)

with engine.begin() as conn:
    for _, row in df.iterrows():
        conn.execute(
            f"""
            update financial_ratios
            set composite_quality_score =
            {row['composite_quality_score']}
            where id = {row['id']}
            """
        )

print("Composite quality scores updated successfully.")