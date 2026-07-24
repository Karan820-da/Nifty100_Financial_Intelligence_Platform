from sqlalchemy import text

from src.dashboard.utils.db import get_engine


def get_company_documents(ticker: str):

    engine = get_engine()

    query = text("""
        SELECT
            year,
            annual_report
        FROM documents
        WHERE company_id = :ticker
        ORDER BY year DESC;
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {"ticker": ticker.upper()})
        rows = result.mappings().all()

    return [dict(row) for row in rows]