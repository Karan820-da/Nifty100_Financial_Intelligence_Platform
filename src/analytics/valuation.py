import sys
from pathlib import Path
import pandas as pd
import numpy as np

# ---------------------------------------------------
# Add src folder to Python path
# ---------------------------------------------------
sys.path.append(str(Path(__file__).resolve().parents[1]))

from dashboard.utils.db import get_engine

# ---------------------------------------------------
# Database Connection
# ---------------------------------------------------
engine = get_engine()

print("✅ Database connected successfully!")

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------
query = """
SELECT
    fr.company_id,
    fr.year,
    c.company_name,
    s.broad_sector,
    s.sub_sector,

    mc.market_cap_crore,
    mc.pe_ratio,
    mc.pb_ratio,
    mc.ev_ebitda,

    fr.free_cash_flow_cr

FROM financial_ratios fr

LEFT JOIN companies c
    ON fr.company_id = c.id

LEFT JOIN sectors s
    ON fr.company_id = s.company_id

LEFT JOIN market_cap mc
    ON fr.company_id = mc.company_id
   AND RIGHT(fr.year,4) = CAST(mc.year AS CHAR)

ORDER BY c.company_name, fr.year;
"""

df = pd.read_sql(query, engine)

print("\n===================================")
print("Data Loaded Successfully")
print("===================================")
print("Original Shape:", df.shape)

# ---------------------------------------------------
# Remove unmatched companies
# ---------------------------------------------------
df = df[df["company_name"].notna()].copy()

print("After removing unmatched rows:", df.shape)

# ---------------------------------------------------
# Convert numeric columns
# ---------------------------------------------------
numeric_cols = [
    "market_cap_crore",
    "pe_ratio",
    "pb_ratio",
    "ev_ebitda",
    "free_cash_flow_cr"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ---------------------------------------------------
# FCF Yield
# ---------------------------------------------------
df["fcf_yield_pct"] = (
    df["free_cash_flow_cr"] /
    df["market_cap_crore"]
) * 100

# ---------------------------------------------------
# Sector Median PE
# ---------------------------------------------------
sector_pe = (
    df.groupby("broad_sector")["pe_ratio"]
      .median()
      .rename("sector_median_pe")
)

df = df.merge(
    sector_pe,
    on="broad_sector",
    how="left"
)

# ---------------------------------------------------
# PE vs Sector Median
# ---------------------------------------------------
df["pe_vs_sector_median_pct"] = (
    (
        df["pe_ratio"] -
        df["sector_median_pe"]
    ) /
    df["sector_median_pe"]
) * 100

# ---------------------------------------------------
# Valuation Flag
# ---------------------------------------------------
def valuation_flag(row):

    pe = row["pe_ratio"]
    median = row["sector_median_pe"]

    if pd.isna(pe) or pd.isna(median):
        return "No Data"

    if pe > median * 1.5:
        return "Caution"

    elif pe < median * 0.7:
        return "Discount"

    else:
        return "Fair"

df["flag"] = df.apply(valuation_flag, axis=1)

# ---------------------------------------------------
# Final Output
# ---------------------------------------------------
valuation_summary = df[
    [
        "company_id",
        "company_name",
        "year",
        "broad_sector",
        "sub_sector",
        "market_cap_crore",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "free_cash_flow_cr",
        "fcf_yield_pct",
        "sector_median_pe",
        "pe_vs_sector_median_pct",
        "flag"
    ]
]

# ---------------------------------------------------
# Save Files
# ---------------------------------------------------
output_dir = Path(__file__).resolve().parents[2] / "output"
output_dir.mkdir(exist_ok=True)

excel_path = output_dir / "valuation_summary.xlsx"
csv_path = output_dir / "valuation_flags.csv"

valuation_summary.to_excel(excel_path, index=False)

valuation_summary[
    [
        "company_id",
        "company_name",
        "year",
        "flag"
    ]
].to_csv(csv_path, index=False)

# ---------------------------------------------------
# Summary
# ---------------------------------------------------
print("\n===================================")
print("Valuation Analysis Complete")
print("===================================")

print("Rows:", len(valuation_summary))
print("Companies:", valuation_summary["company_id"].nunique())

print("\nFlag Distribution:")
print(valuation_summary["flag"].value_counts())

print("\nTop 10 Records:")
print(valuation_summary.head(10))

print("\nFiles Saved Successfully")
print(excel_path)
print(csv_path)