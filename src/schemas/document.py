
from pydantic import BaseModel


class CompanyDocument(BaseModel):

    year: str

    annual_report: str | None = None

    class Config:
        from_attributes = True
