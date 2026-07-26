
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
