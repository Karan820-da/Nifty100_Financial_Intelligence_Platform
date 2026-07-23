from fastapi import APIRouter
from sqlalchemy import text
import time

from src.dashboard.utils.db import get_engine

router = APIRouter()

API_VERSION = "1.0.0"

START_TIME = time.time()


@router.get("/health")
def health():

    engine = get_engine()

    tables = [
        "analysis",
        "balancesheet",
        "cashflow",
        "companies",
        "documents",
        "financial_ratios",
        "market_cap",
        "peer_groups",
        "peer_percentiles",
        "profitandloss",
        "prosandcons",
        "sectors",
        "stock_prices"
    ]

    row_counts = {}

    try:

        with engine.connect() as conn:

            for table in tables:

                try:

                    result = conn.execute(
                        text(f"SELECT COUNT(*) FROM {table}")
                    )

                    row_counts[table] = result.scalar()

                except Exception as e:

                    row_counts[table] = f"Error: {str(e)}"

        return {

            "status": "ok",

            "version": API_VERSION,

            "uptime_seconds": round(
                time.time() - START_TIME,
                2
            ),

            "db_row_counts": row_counts

        }

    except Exception as e:

        return {

            "status": "error",

            "version": API_VERSION,

            "message": str(e)

        }