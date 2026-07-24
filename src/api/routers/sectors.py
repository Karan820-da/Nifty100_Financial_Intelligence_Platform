from fastapi import APIRouter
from typing import List
from src.schemas.sector_company import SectorCompany
from src.schemas.sector import SectorSummary
from src.services.sector_service import (
    get_sector_summary,
    get_companies_by_sector
)
router = APIRouter()


@router.get(
    "/sectors",
    response_model=List[SectorSummary]
)
def list_sectors():

    return get_sector_summary()

@router.get(
    "/sectors/{sector}/companies",
    response_model=list[SectorCompany]
)
def sector_companies(sector: str):

    return get_companies_by_sector(sector)