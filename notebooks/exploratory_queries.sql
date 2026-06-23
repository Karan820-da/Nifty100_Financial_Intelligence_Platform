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

-- Top 10 companies by sales
SELECT company_id, MAX(sales)
FROM profitandloss
GROUP BY company_id
ORDER BY MAX(sales) DESC
LIMIT 10;

-- Top companies by operating profit
SELECT company_id, MAX(operating_profit)
FROM profitandloss
GROUP BY company_id
ORDER BY MAX(operating_profit) DESC
LIMIT 10;

-- Highest reserves
SELECT company_id, MAX(reserves)
FROM balancesheet
GROUP BY company_id
ORDER BY MAX(reserves) DESC
LIMIT 10;

-- Highest borrowings
SELECT company_id, MAX(borrowings)
FROM balancesheet
GROUP BY company_id
ORDER BY MAX(borrowings) DESC
LIMIT 10;

-- Highest net cash flow
SELECT company_id, MAX(net_cash_flow)
FROM cashflow
GROUP BY company_id
ORDER BY MAX(net_cash_flow) DESC
LIMIT 10;

-- Sector wise company count
SELECT sector_name, COUNT(*)
FROM sectors
GROUP BY sector_name;

-- Companies with positive cash flow
SELECT DISTINCT company_id
FROM cashflow
WHERE net_cash_flow > 0;

-- Top market cap companies
SELECT company_id, MAX(market_cap)
FROM market_cap
GROUP BY company_id
ORDER BY MAX(market_cap) DESC
LIMIT 10;

-- Documents count by company
SELECT company_id, COUNT(*)
FROM documents
GROUP BY company_id
ORDER BY COUNT(*) DESC;

-- Analysis records count
SELECT COUNT(*)
FROM analysis;