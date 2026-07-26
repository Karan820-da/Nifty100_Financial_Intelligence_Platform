
from pydantic import BaseModel


class CompanySummary(BaseModel):
    id: str
    company_name: str
    broad_sector: str | None
    sub_sector: str | None
    market_cap_category: str | None
    roe_percentage: float | None
    roce_percentage: float | None

    class Config:
        from_attributes = True


class LatestRatios(BaseModel):
    year: str | None

    net_profit_margin_pct: float | None
    operating_profit_margin_pct: float | None
    return_on_equity_pct: float | None

    debt_to_equity: float | None
    interest_coverage: float | None
    asset_turnover: float | None

    free_cash_flow_cr: float | None
    earnings_per_share: float | None

    revenue_cagr_5yr: float | None
    pat_cagr_5yr: float | None

    class Config:
        from_attributes = True


class CompanyDetail(BaseModel):
    id: str

    company_name: str | None
    company_logo: str | None
    about_company: str | None

    website: str | None
    nse_profile: str | None
    bse_profile: str | None

    face_value: float | None
    book_value: float | None

    roe_percentage: float | None
    roce_percentage: float | None

    broad_sector: str | None
    sub_sector: str | None
    market_cap_category: str | None

    latest_ratios: LatestRatios | None

    class Config:
        from_attributes = True
