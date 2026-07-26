from fastapi import APIRouter

router = APIRouter()


from fastapi import APIRouter

from src.schemas.portfolio import PortfolioStat
from src.services.portfolio_service import get_portfolio_stats

router = APIRouter()


@router.get("/portfolio/stats", response_model=list[PortfolioStat])
def portfolio_stats():

    return get_portfolio_stats()
