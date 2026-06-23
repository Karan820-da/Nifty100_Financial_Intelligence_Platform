select
    company_id,
    max(return_on_equity_pct) as roe
from financial_ratios
group by company_id
order by roe desc
limit 10;

select
    company_id,
    max(net_profit_margin_pct) as npm
from financial_ratios
group by company_id
order by npm desc
limit 10;

select
    company_id,
    min(debt_to_equity) as debt_to_equity
from financial_ratios
group by company_id
order by debt_to_equity asc
limit 10;

select
    company_id,
    max(market_cap_crore) as market_cap
from market_cap
group by company_id
order by market_cap desc
limit 10;

select
    broad_sector,
    count(*) as companies
from sectors
group by broad_sector
order by companies desc;

select
    company_id,
    max(operating_activity) as operating_cash_flow
from cashflow
group by company_id
order by operating_cash_flow desc
limit 10;

select
    company_id,
    count(*) as reports
from documents
group by company_id
order by reports desc;

select
    company_id,
    max(roce_percentage) as roce
from companies
group by company_id
order by roce desc
limit 10;

select
    company_id,
    max(dividend_yield_pct) as dividend_yield
from market_cap
group by company_id
order by dividend_yield desc
limit 10;

select
    peer_group_name,
    count(*) as companies
from peer_groups
group by peer_group_name
order by companies desc;
