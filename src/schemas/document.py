from typing import Optional
from pydantic import BaseModel


class CompanyDocument(BaseModel):

    year: str

    annual_report: Optional[str] = None

    class Config:
        from_attributes = True