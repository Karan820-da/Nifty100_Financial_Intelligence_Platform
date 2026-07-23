from sqlalchemy import text
from pathlib import Path
from src.dashboard.utils.db import get_engine


def get_companies(
    sector=None,
    market_cap_category=None,
    search=None,
):

    engine = get_engine()

    query = text(
        """
        SELECT

            c.id,
            c.company_name,

            s.broad_sector,
            s.sub_sector,
            s.market_cap_category,

            c.roe_percentage,
            c.roce_percentage

        FROM companies c

        LEFT JOIN sectors s
            ON c.id = s.company_id

        WHERE

            (:sector IS NULL
             OR s.broad_sector = :sector)

        AND

            (:market_cap_category IS NULL
             OR s.market_cap_category = :market_cap_category)

        AND

            (
                :search IS NULL
                OR c.company_name LIKE CONCAT('%', :search, '%')
                OR c.id LIKE CONCAT('%', :search, '%')
            )

        ORDER BY c.company_name
        """
    )

    with engine.connect() as conn:

        result = conn.execute(
            query,
            {
                "sector": sector,
                "market_cap_category": market_cap_category,
                "search": search,
            },
        )

        return [dict(row._mapping) for row in result]

from sqlalchemy import text


def get_company_by_ticker(ticker: str):

    engine = get_engine()

    query = text("""
    SELECT

        c.*,

        s.broad_sector,
        s.sub_sector,
        s.market_cap_category,

        fr.year,

        fr.net_profit_margin_pct,
        fr.operating_profit_margin_pct,
        fr.return_on_equity_pct,

        fr.debt_to_equity,
        fr.interest_coverage,
        fr.asset_turnover,

        fr.free_cash_flow_cr,

        fr.earnings_per_share,

        fr.revenue_cagr_5yr,
        fr.pat_cagr_5yr

    FROM companies c

    LEFT JOIN sectors s

        ON c.id = s.company_id

    LEFT JOIN (

        SELECT *

        FROM financial_ratios fr

        INNER JOIN (

            SELECT
                company_id,
                MAX(id) AS latest_id

            FROM financial_ratios

            GROUP BY company_id

        ) latest

        ON fr.id = latest.latest_id

    ) fr

        ON c.id = fr.company_id

    WHERE c.id = :ticker
    """)

    with engine.connect() as conn:

        result = conn.execute(
            query,
            {"ticker": ticker}
        )

        row = result.fetchone()

    if row is None:
        return None

    data = dict(row._mapping)

    latest = {

        "year": data.pop("year"),

        "net_profit_margin_pct":
            data.pop("net_profit_margin_pct"),

        "operating_profit_margin_pct":
            data.pop("operating_profit_margin_pct"),

        "return_on_equity_pct":
            data.pop("return_on_equity_pct"),

        "debt_to_equity":
            data.pop("debt_to_equity"),

        "interest_coverage":
            data.pop("interest_coverage"),

        "asset_turnover":
            data.pop("asset_turnover"),

        "free_cash_flow_cr":
            data.pop("free_cash_flow_cr"),

        "earnings_per_share":
            data.pop("earnings_per_share"),

        "revenue_cagr_5yr":
            data.pop("revenue_cagr_5yr"),

        "pat_cagr_5yr":
            data.pop("pat_cagr_5yr")

    }

    data["latest_ratios"] = latest

    return data

from sqlalchemy import text


def get_profit_loss_history(engine, ticker: str):

    query = text("""
        SELECT
            year,
            sales,
            expenses,
            operating_profit,
            opm_percentage,
            other_income,
            interest,
            depreciation,
            profit_before_tax,
            tax_percentage,
            net_profit,
            eps,
            dividend_payout
        FROM profitandloss
        WHERE company_id = :ticker
        ORDER BY year
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {"ticker": ticker})
        rows = result.mappings().all()

    return [dict(row) for row in rows]

def get_balance_sheet_history(ticker: str):

    engine = get_engine()

    query = text("""
        SELECT
            year,
            equity_capital,
            reserves,
            borrowings,
            other_liabilities,
            total_liabilities,
            fixed_assets,
            cwip,
            investments,
            other_asset,
            total_assets
        FROM balancesheet
        WHERE company_id = :ticker
        ORDER BY year
    """)

    with engine.connect() as conn:

        result = conn.execute(query, {"ticker": ticker})

        rows = result.mappings().all()

    return [dict(row) for row in rows]

def get_cashflow_history(ticker: str):

    engine = get_engine()

    query = text("""
        SELECT
            year,
            operating_activity,
            investing_activity,
            financing_activity,
            net_cash_flow
        FROM cashflow
        WHERE company_id = :ticker
        ORDER BY year
    """)

    with engine.connect() as conn:

        result = conn.execute(query, {"ticker": ticker})

        rows = result.mappings().all()

    return [dict(row) for row in rows]

def get_company_ratios(ticker: str):

    engine = get_engine()

    query = text("""
        SELECT
            year,
            net_profit_margin_pct,
            operating_profit_margin_pct,
            return_on_equity_pct,
            debt_to_equity,
            interest_coverage,
            asset_turnover,
            free_cash_flow_cr,
            capex_cr,
            earnings_per_share,
            book_value_per_share,
            dividend_payout_ratio_pct,
            total_debt_cr,
            cash_from_operations_cr,
            revenue_cagr_5yr,
            pat_cagr_5yr,
            eps_cagr_5yr,
            composite_quality_score
        FROM financial_ratios
        WHERE company_id = :ticker
        ORDER BY year
    """)

    with engine.connect() as conn:

        result = conn.execute(query, {"ticker": ticker})

        rows = result.mappings().all()

    return [dict(row) for row in rows]

def get_tearsheet_path(ticker: str):

    project_root = Path(__file__).resolve().parents[2]

    pdf_path = project_root / "reports" / "tearsheets" / f"{ticker}.pdf"

    return pdf_path