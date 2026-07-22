import os
import sys

import pandas as pd

# ---------------------------------------
# Add src folder
# ---------------------------------------

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from dashboard.utils.db import get_engine

engine = get_engine()

# ---------------------------------------
# Load Tables
# ---------------------------------------

financial = pd.read_sql(
    "SELECT * FROM financial_ratios ORDER BY company_id, year",
    engine
)

profit = pd.read_sql(
    "SELECT * FROM profitandloss ORDER BY company_id, year",
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
print("Financial Ratios :", financial.shape)
print("Profit & Loss    :", profit.shape)
print("Companies        :", companies.shape)

pros_cons = []
# ---------------------------------------
# Helper Function
# ---------------------------------------

def add_signal(
    company,
    signal_type,
    rule_id,
    text,
    confidence
):
    """
    Add a pro/con signal if confidence >= 60
    """

    if confidence >= 60:

        pros_cons.append(
            {
                "company_id": company,
                "type": signal_type,
                "rule_id": rule_id,
                "text": text,
                "confidence_pct": confidence
            }
        )
# ---------------------------------------
# Generate Pro Rules 1–6
# ---------------------------------------

for company in companies["company_id"]:

    fr = (
        financial[financial["company_id"] == company]
        .sort_values("year")
        .reset_index(drop=True)
    )

    pl = (
        profit[profit["company_id"] == company]
        .sort_values("year")
        .reset_index(drop=True)
    )

    if fr.empty or pl.empty:
        continue

    latest_fr = fr.iloc[-1]
    latest_pl = pl.iloc[-1]

    # -----------------------------------
    # Pro Rule 1
    # ROE > 20% for last 3 years
    # -----------------------------------

    if len(fr) >= 3:

        if (fr.tail(3)["return_on_equity_pct"] > 20).all():

            add_signal(
                company,
                "pro",
                "PRO_1",
                "Consistently high return on equity above 20% demonstrates exceptional capital efficiency.",
                95,
            )
        # -----------------------------------
    # Pro Rule 7
    # ICR > 10 OR Debt Free
    # -----------------------------------

    if (
        latest_fr["interest_coverage"] > 10
        or latest_fr["debt_to_equity"] == 0
    ):

        add_signal(
            company,
            "pro",
            "PRO_7",
            "Very high interest coverage ratio reflects negligible financial stress from debt servicing.",
            90,
        )

    # -----------------------------------
    # Pro Rule 9
    # EPS CAGR >15%
    # -----------------------------------

    if latest_fr["eps_cagr_5yr"] > 15:

        add_signal(
            company,
            "pro",
            "PRO_9",
            "Earnings per share growing above 15% CAGR indicates strong earnings quality and compounding.",
            91,
        )

    # -----------------------------------
    # Pro Rule 10
    # ROE improving for 3 years
    # -----------------------------------

    if len(fr) >= 3:

        roe = fr.tail(3)["return_on_equity_pct"].tolist()

        if roe[0] < roe[1] < roe[2]:

            add_signal(
                company,
                "pro",
                "PRO_10",
                "Return on equity improving for 3 consecutive years shows strengthening business quality.",
                87,
            )

    # -----------------------------------
    # Pro Rule 11
    # Revenue CAGR > PAT CAGR
    # (keeping the assignment's rule ID, although the text implies PAT grows faster)
    # -----------------------------------

    if latest_fr["pat_cagr_5yr"] > latest_fr["revenue_cagr_5yr"]:

        add_signal(
            company,
            "pro",
            "PRO_11",
            "Revenue growing slower than profits shows improving operating leverage and scale benefits.",
            90,
        )

    # -----------------------------------
    # Pro Rule 2
    # Positive FCF for 5 years
    # -----------------------------------

    if len(fr) >= 5:

        if (fr.tail(5)["free_cash_flow_cr"] > 0).all():

            add_signal(
                company,
                "pro",
                "PRO_2",
                "Strong free cash flow generation over 5 years signals healthy business fundamentals.",
                92,
            )

    # -----------------------------------
    # Pro Rule 3
    # Debt Free
    # -----------------------------------

    if latest_fr["debt_to_equity"] == 0:

        add_signal(
            company,
            "pro",
            "PRO_3",
            "Debt-free balance sheet provides financial flexibility and eliminates interest burden.",
            100,
        )

    # -----------------------------------
    # Pro Rule 4
    # Revenue CAGR >15%
    # -----------------------------------

    if latest_fr["revenue_cagr_5yr"] > 15:

        add_signal(
            company,
            "pro",
            "PRO_4",
            "Revenue growing at above 15% CAGR over 5 years reflects strong business momentum.",
            90,
        )

    # -----------------------------------
    # Pro Rule 5
    # OPM >25%
    # -----------------------------------

    if latest_pl["opm_percentage"] > 25:

        add_signal(
            company,
            "pro",
            "PRO_5",
            "Operating profit margin above 25% indicates strong pricing power and cost discipline.",
            88,
        )

    # -----------------------------------
    # Pro Rule 6
    # PAT CAGR >20%
    # -----------------------------------

    if latest_fr["pat_cagr_5yr"] > 20:

        add_signal(
            company,
            "pro",
            "PRO_6",
            "Net profit compounding at above 20% over 5 years creates significant shareholder value.",
            93,
        )

    # -----------------------------------
    # Con Rule 1
    # Debt to Equity > 2
    # -----------------------------------

    if latest_fr["debt_to_equity"] > 2:

        add_signal(
            company,
            "con",
            "CON_1",
            "High debt-to-equity ratio indicates elevated financial leverage and risk.",
            95,
        )

    # -----------------------------------
    # Con Rule 2
    # Negative Free Cash Flow for 3 Years
    # -----------------------------------

    if len(fr) >= 3:

        if (fr.tail(3)["free_cash_flow_cr"] < 0).all():

            add_signal(
                company,
                "con",
                "CON_2",
                "Negative free cash flow for three consecutive years raises concerns about cash generation.",
                92,
            )

    # -----------------------------------
    # Con Rule 3
    # Operating Margin Declining
    # -----------------------------------

    if len(pl) >= 3:

        opm = pl.tail(3)["opm_percentage"].tolist()

        if opm[0] > opm[1] > opm[2]:

            add_signal(
                company,
                "con",
                "CON_3",
                "Operating margins have declined for three consecutive years.",
                88,
            )

    # -----------------------------------
    # Con Rule 4
    # Latest Net Profit Negative
    # -----------------------------------

    if latest_pl["net_profit"] < 0:

        add_signal(
            company,
            "con",
            "CON_4",
            "Company reported a net loss in the latest financial year.",
            96,
        )
        # -----------------------------------
    # Con Rule 5
    # Revenue declining for 2 years
    # -----------------------------------

    if len(pl) >= 3:

        sales = pl.tail(3)["sales"].tolist()

        if sales[0] > sales[1] > sales[2]:

            add_signal(
                company,
                "con",
                "CON_5",
                "Revenue has declined for consecutive years, indicating weakening business momentum.",
                90,
            )

    # -----------------------------------
    # Con Rule 6
    # Interest Coverage < 1.5
    # -----------------------------------

    if latest_fr["interest_coverage"] < 1.5:

        add_signal(
            company,
            "con",
            "CON_6",
            "Low interest coverage indicates difficulty servicing debt obligations.",
            94,
        )

    # -----------------------------------
    # Con Rule 7
    # Dividend payout >100%
    # -----------------------------------

    if latest_pl["dividend_payout"] > 100:

        add_signal(
            company,
            "con",
            "CON_7",
            "Dividend payout exceeds earnings, which may not be sustainable.",
            89,
        )

    # -----------------------------------
    # Con Rule 8
    # Debt increasing for 3 years
    # -----------------------------------

    if len(fr) >= 3:

        debt = fr.tail(3)["debt_to_equity"].tolist()

        if debt[0] < debt[1] < debt[2]:

            add_signal(
                company,
                "con",
                "CON_8",
                "Debt levels have increased consistently over the last three years.",
                91,
            )

    # -----------------------------------
    # Con Rule 9
    # EPS declining for 3 years
    # -----------------------------------

    if len(pl) >= 3:

        eps = pl.tail(3)["eps"].tolist()

        if eps[0] > eps[1] > eps[2]:

            add_signal(
                company,
                "con",
                "CON_9",
                "Earnings per share have declined consistently over three years.",
                90,
            )

        # -----------------------------------
    # Con Rule 12
    # Revenue CAGR < 5%
    # -----------------------------------

    if latest_fr["revenue_cagr_5yr"] < 5:

        add_signal(
            company,
            "con",
            "CON_12",
            "Revenue growth below 5% over five years indicates weak long-term business expansion.",
            88,
        )

# ---------------------------------------
# Build DataFrame
# ---------------------------------------

pros_df = pd.DataFrame(pros_cons)

# ---------------------------------------
# Fallback Pro Signals
# ---------------------------------------

for company in companies["company_id"]:

    has_pro = (
        (pros_df["company_id"] == company) &
        (pros_df["type"] == "pro")
    ).any()

    if not has_pro:

        add_signal(
            company,
            "pro",
            "PRO_DEFAULT",
            "Company demonstrates stable financial performance but does not currently satisfy any major positive screening rule.",
            60,
        )

# ---------------------------------------
# Rebuild DataFrame
# ---------------------------------------

pros_df = pd.DataFrame(pros_cons)

# ---------------------------------------
# Fallback Con Signals
# ---------------------------------------

for company in companies["company_id"]:

    has_con = (
        (pros_df["company_id"] == company) &
        (pros_df["type"] == "con")
    ).any()

    if not has_con:

        add_signal(
            company,
            "con",
            "CON_DEFAULT",
            "No significant financial weaknesses were detected by the rule engine. Future performance should continue to be monitored.",
            60,
        )

# ---------------------------------------
# Final DataFrame
# ---------------------------------------

pros_df = pd.DataFrame(pros_cons)
print(f"\nSignals Generated : {len(pros_cons)}")

pros_df = pd.DataFrame(pros_cons)

print(pros_df.head(20))
# ---------------------------------------
# Save Output
# ---------------------------------------

os.makedirs("output", exist_ok=True)

pros_df.to_csv(
    "output/pros_cons_generated.csv",
    index=False
)

print("\nOutput Saved Successfully!")
print("Saved to: output/pros_cons_generated.csv")

# ---------------------------------------
# Validation
# ---------------------------------------

pros_df = pd.DataFrame(pros_cons)

print("\n========== VALIDATION ==========")

total_companies = companies["company_id"].nunique()

pro_companies = pros_df[pros_df["type"] == "pro"]["company_id"].nunique()
con_companies = pros_df[pros_df["type"] == "con"]["company_id"].nunique()

print(f"Total Companies : {total_companies}")
print(f"Companies with Pros : {pro_companies}")
print(f"Companies with Cons : {con_companies}")

missing_pro = sorted(
    set(companies["company_id"]) -
    set(pros_df[pros_df["type"] == "pro"]["company_id"])
)

missing_con = sorted(
    set(companies["company_id"]) -
    set(pros_df[pros_df["type"] == "con"]["company_id"])
)

print("\nMissing Pro Signals :", len(missing_pro))
print(missing_pro)

print("\nMissing Con Signals :", len(missing_con))
print(missing_con)

