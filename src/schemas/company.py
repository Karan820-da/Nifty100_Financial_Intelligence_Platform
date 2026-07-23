from typing import Optional

from pydantic import BaseModel


class CompanySummary(BaseModel):
    id: str
    company_name: str
    broad_sector: Optional[str]
    sub_sector: Optional[str]
    market_cap_category: Optional[str]
    roe_percentage: Optional[float]
    roce_percentage: Optional[float]

    class Config:
        from_attributes = True


class LatestRatios(BaseModel):
    year: Optional[str]

    net_profit_margin_pct: Optional[float]
    operating_profit_margin_pct: Optional[float]
    return_on_equity_pct: Optional[float]

    debt_to_equity: Optional[float]
    interest_coverage: Optional[float]
    asset_turnover: Optional[float]

    free_cash_flow_cr: Optional[float]
    earnings_per_share: Optional[float]

    revenue_cagr_5yr: Optional[float]
    pat_cagr_5yr: Optional[float]

    class Config:
        from_attributes = True


class CompanyDetail(BaseModel):
    id: str

    company_name: Optional[str]
    company_logo: Optional[str]
    about_company: Optional[str]

    website: Optional[str]
    nse_profile: Optional[str]
    bse_profile: Optional[str]

    face_value: Optional[float]
    book_value: Optional[float]

    roe_percentage: Optional[float]
    roce_percentage: Optional[float]

    broad_sector: Optional[str]
    sub_sector: Optional[str]
    market_cap_category: Optional[str]

    latest_ratios: Optional[LatestRatios]

    class Config:
        from_attributes = True