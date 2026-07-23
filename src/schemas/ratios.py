from typing import Optional
from pydantic import BaseModel


class RatioRecord(BaseModel):

    year: Optional[str]

    net_profit_margin_pct: Optional[float]
    operating_profit_margin_pct: Optional[float]
    return_on_equity_pct: Optional[float]
    debt_to_equity: Optional[float]
    interest_coverage: Optional[float]
    asset_turnover: Optional[float]
    free_cash_flow_cr: Optional[float]
    capex_cr: Optional[float]
    earnings_per_share: Optional[float]
    book_value_per_share: Optional[float]
    dividend_payout_ratio_pct: Optional[float]
    total_debt_cr: Optional[float]
    cash_from_operations_cr: Optional[float]
    revenue_cagr_5yr: Optional[float]
    pat_cagr_5yr: Optional[float]
    eps_cagr_5yr: Optional[float]
    composite_quality_score: Optional[float]

    class Config:
        from_attributes = True