from fastapi import APIRouter

router = APIRouter()

from typing import List
from fastapi import APIRouter, Query

from src.schemas.screener import ScreenerResult
from src.services.screener_service import screen_companies

router = APIRouter()


@router.get(
    "/screener",
    response_model=List[ScreenerResult],
)
def screener(
    min_roe: float = Query(15),
    max_de: float = Query(1),
    max_pe: float = Query(30),
    min_market_cap: float = Query(1000),
):
    return screen_companies(
        min_roe=min_roe,
        max_de=max_de,
        max_pe=max_pe,
        min_market_cap=min_market_cap,
    )