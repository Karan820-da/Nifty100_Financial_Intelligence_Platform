from typing import List

from fastapi import APIRouter

from src.schemas.market_cap import MarketCapHistory
from src.services.market_cap_service import get_market_cap_history

router = APIRouter()


@router.get(
    "/market-cap/{ticker}",
    response_model=List[MarketCapHistory]
)
def market_cap_history(ticker: str):

    return get_market_cap_history(ticker)