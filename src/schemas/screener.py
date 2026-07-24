from pydantic import BaseModel
from typing import Optional


class ScreenerResult(BaseModel):
    company_id: str
    company_name: str
    broad_sector: Optional[str] = None
    return_on_equity_pct: Optional[float] = None
    debt_to_equity: Optional[float] = None
    pe_ratio: Optional[float] = None
    market_cap_crore: Optional[float] = None

    class Config:
        from_attributes = True