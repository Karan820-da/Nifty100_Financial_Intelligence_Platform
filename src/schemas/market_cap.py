
from pydantic import BaseModel


class MarketCapHistory(BaseModel):

    year: str

    market_cap_crore: float | None = None

    enterprise_value_crore: float | None = None

    pe_ratio: float | None = None

    pb_ratio: float | None = None

    ev_ebitda: float | None = None

    dividend_yield_pct: float | None = None

    class Config:
        from_attributes = True
