from typing import Optional
from pydantic import BaseModel


class MarketCapHistory(BaseModel):

    year: str

    market_cap_crore: Optional[float] = None

    enterprise_value_crore: Optional[float] = None

    pe_ratio: Optional[float] = None

    pb_ratio: Optional[float] = None

    ev_ebitda: Optional[float] = None

    dividend_yield_pct: Optional[float] = None

    class Config:
        from_attributes = True