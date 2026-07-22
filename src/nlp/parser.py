import os
import sys
import re
import pandas as pd

# -------------------------------------------------
# Add src folder to Python path
# -------------------------------------------------
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from dashboard.utils.db import get_engine

# -------------------------------------------------
# Load Analysis Table
# -------------------------------------------------
engine = get_engine()

query = """
SELECT
    company_id,
    compounded_sales_growth,
    compounded_profit_growth,
    stock_price_cagr,
    roe
FROM analysis;
"""

df = pd.read_sql(query, engine)

print(f"Loaded {len(df)} records from analysis table.")

# -------------------------------------------------
# Regex Patterns
# -------------------------------------------------
patterns = {
    "years": r"(\d+)\s*Years?:?\s*(-?[\d.]+)%",
    "last_year": r"Last\s*Year:?\s*(-?[\d.]+)%",
    "ttm": r"TTM:?\s*(-?[\d.]+)%"
}

metrics = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe"
]

parsed_rows = []
failed_rows = []

# -------------------------------------------------
# Parse Text
# -------------------------------------------------
for _, row in df.iterrows():

    company = row["company_id"]

    for metric in metrics:

        text = row[metric]

        if pd.isna(text):
            continue

        text = str(text).strip()

        matched = False

        # -----------------------------
        # Pattern 1: X Years
        # -----------------------------
        match = re.search(patterns["years"], text, re.IGNORECASE)

        if match:
            parsed_rows.append({
                "company_id": company,
                "metric_type": metric,
                "period_years": int(match.group(1)),
                "value_pct": float(match.group(2))
            })
            matched = True

        # -----------------------------
        # Pattern 2: Last Year
        # -----------------------------
        if not matched:

            match = re.search(
                patterns["last_year"],
                text,
                re.IGNORECASE
            )

            if match:

                parsed_rows.append({
                    "company_id": company,
                    "metric_type": metric,
                    "period_years": 1,
                    "value_pct": float(match.group(1))
                })

                matched = True

        # -----------------------------
        # Pattern 3: TTM
        # -----------------------------
        if not matched:

            match = re.search(
                patterns["ttm"],
                text,
                re.IGNORECASE
            )

            if match:

                parsed_rows.append({
                    "company_id": company,
                    "metric_type": metric,
                    "period_years": 0,
                    "value_pct": float(match.group(1))
                })

                matched = True

        # -----------------------------
        # Failed Parsing
        # -----------------------------
        if not matched:

            failed_rows.append({
                "company_id": company,
                "metric_type": metric,
                "original_text": text
            })

# -------------------------------------------------
# Create Output Folder
# -------------------------------------------------
os.makedirs("output", exist_ok=True)

parsed_df = pd.DataFrame(parsed_rows)
failed_df = pd.DataFrame(failed_rows)

# -------------------------------------------------
# Save Outputs
# -------------------------------------------------
parsed_df.to_csv(
    "output/analysis_parsed.csv",
    index=False
)

failed_df.to_csv(
    "output/parse_failures.csv",
    index=False
)

# -------------------------------------------------
# Summary
# -------------------------------------------------
print("\n========== Parsing Summary ==========")
print(f"Total Companies : {df['company_id'].nunique()}")
print(f"Parsed Records  : {len(parsed_df)}")
print(f"Failed Records  : {len(failed_df)}")

print("\nFiles Generated")
print("---------------------------")
print("output/analysis_parsed.csv")
print("output/parse_failures.csv")