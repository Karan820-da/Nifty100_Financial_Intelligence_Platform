
from fastapi import APIRouter

from src.schemas.sector import SectorSummary
from src.schemas.sector_company import SectorCompany
from src.services.sector_service import get_companies_by_sector, get_sector_summary

router = APIRouter()


@router.get("/sectors", response_model=list[SectorSummary])
def list_sectors():

    return get_sector_summary()


@router.get("/sectors/{sector}/companies", response_model=list[SectorCompany])
def sector_companies(sector: str):

    return get_companies_by_sector(sector)
