
from pydantic import BaseModel


class CashFlowRecord(BaseModel):

    year: str | None

    operating_activity: float | None
    investing_activity: float | None
    financing_activity: float | None
    net_cash_flow: float | None

    class Config:
        from_attributes = True
