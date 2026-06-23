SELECT COUNT(*) FROM companies;

SELECT company_name, roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;

SELECT company_id, AVG(net_profit)
FROM profitandloss
GROUP BY company_id;

SELECT company_id, AVG(close_price)
FROM stock_prices
GROUP BY company_id;

SELECT company_id, MAX(market_cap_crore)
FROM market_cap
GROUP BY company_id;

SELECT company_id, AVG(return_on_equity_pct)
FROM financial_ratio
GROUP BY company_id;

SELECT broad_sector, COUNT(*)
FROM sectors
GROUP BY broad_sector;

SELECT COUNT(*) FROM balancesheet;

SELECT COUNT(*) FROM cashflow;

SELECT COUNT(*) FROM analysis;