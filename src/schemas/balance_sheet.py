
from pydantic import BaseModel


class BalanceSheetRecord(BaseModel):

    year: str | None

    equity_capital: float | None
    reserves: float | None
    borrowings: float | None
    other_liabilities: float | None
    total_liabilities: float | None

    fixed_assets: float | None
    cwip: float | None
    investments: float | None
    other_asset: float | None
    total_assets: float | None

    class Config:
        from_attributes = True
