from sqlalchemy import text

from src.dashboard.utils.db import get_engine


def screen_companies(
    min_roe: float = 15,
    max_de: float = 1,
    max_pe: float = 30,
    min_market_cap: float = 1000
):
    engine = get_engine()

    query = text("""
        SELECT
            c.id AS company_id,
            c.company_name,
            s.broad_sector,
            fr.return_on_equity_pct,
            fr.debt_to_equity,
            mc.pe_ratio,
            mc.market_cap_crore
        FROM companies c

        JOIN financial_ratios fr
            ON c.id = fr.company_id

        JOIN sectors s
            ON c.id = s.company_id

        JOIN market_cap mc
            ON c.id = mc.company_id

        WHERE
            fr.return_on_equity_pct >= :min_roe
            AND fr.debt_to_equity <= :max_de
            AND mc.pe_ratio <= :max_pe
            AND mc.market_cap_crore >= :min_market_cap

        ORDER BY
            fr.return_on_equity_pct DESC;
    """)

    with engine.connect() as conn:
        rows = conn.execute(
            query,
            {
                "min_roe": min_roe,
                "max_de": max_de,
                "max_pe": max_pe,
                "min_market_cap": min_market_cap,
            },
        ).mappings().all()

    return [dict(row) for row in rows]