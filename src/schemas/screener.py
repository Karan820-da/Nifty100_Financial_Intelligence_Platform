
from pydantic import BaseModel


class ScreenerResult(BaseModel):
    company_id: str
    company_name: str
    broad_sector: str | None = None
    return_on_equity_pct: float | None = None
    debt_to_equity: float | None = None
    pe_ratio: float | None = None
    market_cap_crore: float | None = None

    class Config:
        from_attributes = True
