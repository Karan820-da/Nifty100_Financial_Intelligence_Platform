
from pydantic import BaseModel


class SectorSummary(BaseModel):

    sector: str

    company_count: int

    median_roe: float | None

    median_pe: float | None

    median_de: float | None

    class Config:
        from_attributes = True
