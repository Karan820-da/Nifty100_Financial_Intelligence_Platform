
from pydantic import BaseModel


class SectorCompany(BaseModel):

    id: str
    company_name: str

    company_logo: str | None = None

    website: str | None = None

    roce_percentage: float | None = None

    roe_percentage: float | None = None

    class Config:
        from_attributes = True
