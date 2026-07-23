from typing import Optional
from pydantic import BaseModel


class BalanceSheetRecord(BaseModel):

    year: Optional[str]

    equity_capital: Optional[float]
    reserves: Optional[float]
    borrowings: Optional[float]
    other_liabilities: Optional[float]
    total_liabilities: Optional[float]

    fixed_assets: Optional[float]
    cwip: Optional[float]
    investments: Optional[float]
    other_asset: Optional[float]
    total_assets: Optional[float]

    class Config:
        from_attributes = True