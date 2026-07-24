from typing import Optional
from pydantic import BaseModel


class SectorSummary(BaseModel):

    sector: str

    company_count: int

    median_roe: Optional[float]

    median_pe: Optional[float]

    median_de: Optional[float]

    class Config:
        from_attributes = True

    