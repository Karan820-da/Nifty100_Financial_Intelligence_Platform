"""
Sprint 5 - Day 31
Cash Flow Intelligence Module
"""

import numpy as np
import pandas as pd

from src.dashboard.utils.db import get_engine

from src.analytics.cashflow_kpis import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate,
    capital_allocation_pattern
)

# ==========================================================
# Database Connection
# ==========================================================

engine = get_engine()

# ==========================================================
# Load Tables
# ==========================================================

cashflow = pd.read_sql(
    """
    SELECT *
    FROM cashflow
    """,
    engine
)

profit = pd.read_sql(
    """
    SELECT *
    FROM profitandloss
    """,
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

# ----------------------------------------------------------
# Clean Company IDs
# ----------------------------------------------------------

cashflow["company_id"] = (
    cashflow["company_id"]
    .astype(str)
    .str.strip()
)

profit["company_id"] = (
    profit["company_id"]
    .astype(str)
    .str.strip()
)

companies["company_id"] = (
    companies["company_id"]
    .astype(str)
    .str.strip()
)

print("Cashflow :", cashflow.shape)
print("Profit   :", profit.shape)
print("Companies:", companies.shape)

# ==========================================================
# Merge Data
# ==========================================================

df = cashflow.merge(
    profit,
    on=["company_id", "year"],
    how="inner"
)

df = df.merge(
    companies,
    on="company_id",
    how="left"
)

# ==========================================================
# Remove Duplicate Company-Year Records
# ==========================================================

df = df.drop_duplicates(
    subset=["company_id", "year"],
    keep="first"
)

# ==========================================================
# Extract Numeric Year
# ==========================================================

df["year_num"] = (
    df["year"]
    .str.extract(r"(\d{4})")
    .astype(int)
)

# ==========================================================
# Fill Missing Company Names
# ==========================================================

df["company_name"] = (
    df["company_name"]
    .fillna(df["company_id"])
)

print(
    "\nCompanies Processed:",
    df["company_id"].nunique()
)

# ==========================================================
# Results Containers
# ==========================================================

results = []

distress_results = []

valid_companies = sorted(
    df["company_id"].unique()
)

print(
    f"Processing {len(valid_companies)} companies..."
)

# ==========================================================
# Process Each Company
# ==========================================================

for company in valid_companies:

    company_df = (
        df[df["company_id"] == company]
        .sort_values("year_num")
        .tail(5)
        .reset_index(drop=True)
    )

    latest = company_df.iloc[-1]

    company_name = latest["company_name"]

    sector = "Unknown"

    # ------------------------------------------------------
    # CFO Quality
    # ------------------------------------------------------

    ratios = (
        company_df["operating_activity"] /
        company_df["net_profit"].replace(0, np.nan)
    )

    cfo_score = ratios.mean()

    cfo_label = cfo_quality_score(
        company_df["operating_activity"].mean(),
        company_df["net_profit"].mean()
    )

    if cfo_label is None:
        cfo_label = "Insufficient Data"
            # ------------------------------------------------------
    # CapEx Intensity
    # ------------------------------------------------------

    latest_sales = latest["sales"]
    latest_cfi = latest["investing_activity"]

    if latest_sales == 0:
        capex_pct = np.nan
        capex_label = "Unknown"
    else:
        capex_pct = (
            abs(latest_cfi) / latest_sales
        ) * 100

        capex_label = capex_intensity(
            latest_cfi,
            latest_sales
        )

    # ------------------------------------------------------
    # Free Cash Flow
    # ------------------------------------------------------

    company_df["fcf"] = company_df.apply(
        lambda row: free_cash_flow(
            row["operating_activity"],
            row["investing_activity"]
        ),
        axis=1
    )

    latest_fcf = company_df["fcf"].iloc[-1]

    # ------------------------------------------------------
    # 5-Year FCF CAGR
    # ------------------------------------------------------

    first_fcf = company_df["fcf"].iloc[0]

    if (
        len(company_df) >= 5
        and first_fcf > 0
        and latest_fcf > 0
    ):
        fcf_cagr = (
            (
                latest_fcf / first_fcf
            ) ** (1 / 4) - 1
        ) * 100
    else:
        fcf_cagr = np.nan

    # ------------------------------------------------------
    # FCF Conversion
    # ------------------------------------------------------

    latest_op = latest["operating_profit"]

    fcf_conversion = fcf_conversion_rate(
        latest_fcf,
        latest_op
    )

    # ------------------------------------------------------
    # Distress Signal
    # ------------------------------------------------------

    latest_cfo = latest["operating_activity"]
    latest_cff = latest["financing_activity"]

    distress_flag = (
        latest_cfo < 0
        and
        latest_cff > 0
    )

    if distress_flag:

        distress_results.append({

            "company_id": company,

            "company_name": company_name,

            "operating_activity": latest_cfo,

            "financing_activity": latest_cff,

            "net_profit": latest["net_profit"]

        })

    # ------------------------------------------------------
    # Deleveraging Flag
    # ------------------------------------------------------
    #
    # Borrowings are not available in the dataset.
    # Using negative financing activity as a proxy.
    # ------------------------------------------------------

    deleveraging_flag = (
        latest_cff < 0
    )

    # ------------------------------------------------------
    # Capital Allocation Pattern
    # ------------------------------------------------------

    capital_label = capital_allocation_pattern(
        latest_cfo,
        latest["investing_activity"],
        latest_cff,
        cfo_label
    )

    # ------------------------------------------------------
    # Store Results
    # ------------------------------------------------------

    results.append({

        "company_id": company,

        "company_name": company_name,

        "sector": sector,

        "cfo_quality_score":
            round(cfo_score, 2)
            if pd.notna(cfo_score)
            else np.nan,

        "cfo_quality_label":
            cfo_label,

        "capex_intensity_pct":
            round(capex_pct, 2)
            if pd.notna(capex_pct)
            else np.nan,

        "capex_label":
            capex_label,

        "fcf_cagr_5yr":
            round(fcf_cagr, 2)
            if pd.notna(fcf_cagr)
            else np.nan,

        "fcf_conversion_pct":
            fcf_conversion,

        "distress_flag":
            distress_flag,

        "deleveraging_flag":
            deleveraging_flag,

        "capital_allocation_label":
            capital_label

    })

# ==========================================================
# Create Output DataFrames
# ==========================================================

results_df = pd.DataFrame(results)

distress_df = pd.DataFrame(distress_results)

# ==========================================================
# Create Output Folder
# ==========================================================

from pathlib import Path

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

# ==========================================================
# Export Cash Flow Intelligence
# ==========================================================

results_df = results_df.sort_values(
    "company_id"
).reset_index(drop=True)

results_df.to_excel(
    output_dir / "cashflow_intelligence.xlsx",
    index=False
)

# ==========================================================
# Export Distress Alerts
# ==========================================================

distress_df.to_csv(
    output_dir / "distress_alerts.csv",
    index=False
)

# ==========================================================
# Summary
# ==========================================================

print("\n" + "=" * 60)
print("Cash Flow Intelligence Module Completed")
print("=" * 60)

print(f"Companies Analysed      : {len(results_df)}")
print(f"Distress Signals Found  : {len(distress_df)}")

print("\nFiles Generated")

print(f"✓ {output_dir / 'cashflow_intelligence.xlsx'}")
print(f"✓ {output_dir / 'distress_alerts.csv'}")

print("=" * 60)

# ==========================================================
# Preview
# ==========================================================

print("\nCash Flow Intelligence Preview\n")

print(results_df.head())

if not distress_df.empty:

    print("\nDistress Alerts Preview\n")

    print(distress_df.head())

else:

    print("\nNo Distress Signals Detected.")

