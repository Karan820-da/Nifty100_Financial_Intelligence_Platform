from sqlalchemy import text

from src.dashboard.utils.db import get_engine


def get_market_cap_history(ticker: str):

    engine = get_engine()

    query = text("""
        SELECT
            year,
            market_cap_crore,
            enterprise_value_crore,
            pe_ratio,
            pb_ratio,
            ev_ebitda,
            dividend_yield_pct
        FROM market_cap
        WHERE company_id = :ticker
        ORDER BY year;
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {"ticker": ticker.upper()})
        rows = result.mappings().all()

    return [dict(row) for row in rows]
