from typing import Optional
from pydantic import BaseModel


class ProfitLossRecord(BaseModel):

    year: Optional[str]

    sales: Optional[float]
    expenses: Optional[float]

    operating_profit: Optional[float]
    opm_percentage: Optional[float]

    other_income: Optional[float]

    interest: Optional[float]

    depreciation: Optional[float]

    profit_before_tax: Optional[float]

    tax_percentage: Optional[float]

    net_profit: Optional[float]

    eps: Optional[float]

    dividend_payout: Optional[float]

    class Config:
        from_attributes = True
        