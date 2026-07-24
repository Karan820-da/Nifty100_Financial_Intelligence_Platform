from fastapi import APIRouter

router = APIRouter()

from typing import List

from fastapi import APIRouter

from src.schemas.document import CompanyDocument
from src.services.document_service import get_company_documents

router = APIRouter()


@router.get(
    "/companies/{ticker}/documents",
    response_model=List[CompanyDocument]
)
def company_documents(ticker: str):

    return get_company_documents(ticker)