
from pydantic import BaseModel


class ProfitLossRecord(BaseModel):

    year: str | None

    sales: float | None
    expenses: float | None

    operating_profit: float | None
    opm_percentage: float | None

    other_income: float | None

    interest: float | None

    depreciation: float | None

    profit_before_tax: float | None

    tax_percentage: float | None

    net_profit: float | None

    eps: float | None

    dividend_payout: float | None

    class Config:
        from_attributes = True
