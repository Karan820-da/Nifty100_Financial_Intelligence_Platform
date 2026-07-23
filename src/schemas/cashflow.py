from typing import Optional
from pydantic import BaseModel


class CashFlowRecord(BaseModel):

    year: Optional[str]

    operating_activity: Optional[float]
    investing_activity: Optional[float]
    financing_activity: Optional[float]
    net_cash_flow: Optional[float]

    class Config:
        from_attributes = True