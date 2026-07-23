from fastapi import HTTPException

from src.schemas.company import CompanyDetail

from src.services.company_service import get_company_by_ticker
from typing import Optional, List
from src.schemas.balance_sheet import BalanceSheetRecord
from src.schemas.cashflow import CashFlowRecord
from src.schemas.ratios import RatioRecord
from fastapi.responses import FileResponse
from fastapi import APIRouter

from src.schemas.company import CompanySummary
from src.services.company_service import get_companies
from src.schemas.history import ProfitLossRecord
from src.services.company_service import get_profit_loss_history
from src.services.company_service import get_balance_sheet_history
from src.services.company_service import get_cashflow_history
from src.services.company_service import get_company_ratios
from src.services.company_service import get_tearsheet_path

router = APIRouter()


@router.get(
    "/companies",
    response_model=List[CompanySummary]
)
def list_companies(

    sector: Optional[str] = None,

    market_cap_category: Optional[str] = None,

    search: Optional[str] = None,

):

    return get_companies(
        sector,
        market_cap_category,
        search,
    )

@router.get(
    "/companies/{ticker}",
    response_model=CompanyDetail
)
def company_profile(ticker: str):

    company = get_company_by_ticker(ticker)

    if company is None:

        raise HTTPException(

            status_code=404,

            detail="Company not found"

        )

    return company

@router.get(
    "/companies/{ticker}/pl",
    response_model=List[ProfitLossRecord]
)
def company_profit_loss(ticker: str):

    data = get_profit_loss_history(ticker)

    if not data:

        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return 
    
@router.get(
    "/companies/{ticker}/bs",
    response_model=List[BalanceSheetRecord]
)
def company_balance_sheet(ticker: str):

    data = get_balance_sheet_history(ticker)

    if not data:

        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return data

@router.get(
    "/companies/{ticker}/cashflow",
    response_model=List[CashFlowRecord]
)
def company_cashflow(ticker: str):

    data = get_cashflow_history(ticker)

    if not data:

        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return data

@router.get(
    "/companies/{ticker}/ratios",
    response_model=List[RatioRecord]
)
def company_ratios(ticker: str):

    data = get_company_ratios(ticker)

    if not data:

        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return data

@router.get("/companies/{ticker}/tearsheet")
def company_tearsheet(ticker: str):

    pdf_path = get_tearsheet_path(ticker)

    if not pdf_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Tearsheet not found"
        )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"{ticker}.pdf"
    )