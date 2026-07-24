from sqlalchemy import text
from src.dashboard.utils.db import get_engine


def get_sector_summary():

    engine = get_engine()

    query = text("""
        SELECT
            s.broad_sector AS sector,
            COUNT(DISTINCT s.company_id) AS company_count,
            ROUND(AVG(fr.return_on_equity_pct), 2) AS median_roe,
            ROUND(AVG(mc.pe_ratio), 2) AS median_pe,
            ROUND(AVG(fr.debt_to_equity), 2) AS median_de
        FROM sectors s

        LEFT JOIN (
            SELECT f.*
            FROM financial_ratios f
            INNER JOIN (
                SELECT company_id, MAX(id) AS latest_id
                FROM financial_ratios
                GROUP BY company_id
            ) latest
            ON f.id = latest.latest_id
        ) fr
        ON s.company_id = fr.company_id

        LEFT JOIN market_cap mc
            ON s.company_id = mc.company_id
           AND mc.year = '2024'

        GROUP BY s.broad_sector

        ORDER BY s.broad_sector;
    """)

    with engine.connect() as conn:
        result = conn.execute(query)
        rows = result.mappings().all()

    return [dict(row) for row in rows]

def get_companies_by_sector(sector: str):

    engine = get_engine()

    query = text("""
        SELECT
            c.id,
            c.company_name,
            c.company_logo,
            c.website,
            c.roce_percentage,
            c.roe_percentage
        FROM sectors s
        JOIN companies c
            ON s.company_id = c.id
        WHERE LOWER(s.broad_sector) = LOWER(:sector)
        ORDER BY c.company_name;
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {"sector": sector})
        rows = result.mappings().all()

    return [dict(row) for row in rows]