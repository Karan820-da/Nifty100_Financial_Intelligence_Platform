from typing import Optional
from pydantic import BaseModel


class PortfolioStat(BaseModel):

    metric: str

    value: Optional[float] = None

    class Config:
        from_attributes = True

from pydantic import BaseModel


class PortfolioStat(BaseModel):

    kpi: str

    p10: float

    p25: float

    p50: float

    p75: float

    p90: float

    mean: float

    std: float

    class Config:
        from_attributes = True