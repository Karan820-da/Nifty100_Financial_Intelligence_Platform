from pydantic import BaseModel
from typing import Optional


class SectorCompany(BaseModel):

    id: str
    company_name: str

    company_logo: Optional[str] = None

    website: Optional[str] = None

    roce_percentage: Optional[float] = None

    roe_percentage: Optional[float] = None

    class Config:
        from_attributes = True