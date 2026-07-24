from sqlalchemy import text

from src.dashboard.utils.db import get_engine


def get_peer_group(group_name: str):

    engine = get_engine()

    query = text("""
        SELECT
            pg.company_id,
            c.company_name,
            c.company_logo,
            pg.peer_group_name,
            pg.is_benchmark
        FROM peer_groups pg
        JOIN companies c
            ON pg.company_id = c.id
        WHERE LOWER(pg.peer_group_name) = LOWER(:group_name)
        ORDER BY
            pg.is_benchmark DESC,
            c.company_name;
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {"group_name": group_name})
        rows = result.mappings().all()

    return [dict(row) for row in rows]