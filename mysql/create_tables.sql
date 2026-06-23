-- =====================================================
-- Nifty100 Financial Intelligence Platform
-- Database Schema
-- Table: companies
-- =====================================================

USE nifty100_db;

CREATE TABLE companies (
    id INT PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    company_logo TEXT,
    chart_link TEXT,
    about_company TEXT,
    website VARCHAR(255),
    nse_profile VARCHAR(255),
    bse_profile VARCHAR(255),
    face_value DECIMAL(10,2),
    book_value DECIMAL(10,2),
    roce_percentage DECIMAL(10,2),
    roe_percentage DECIMAL(10,2)
);
-- =====================================================
-- Table: balancesheet
-- =====================================================

create table balancesheet (
    id int primary key,

    company_id varchar(20) not null,

    year varchar(20),

    equity_capital decimal(15,2),
    reserves decimal(15,2),
    borrowings decimal(15,2),
    other_liabilities decimal(15,2),
    total_liabilities decimal(15,2),

    fixed_assets decimal(15,2),
    cwip decimal(15,2),
    investments decimal(15,2),
    other_asset decimal(15,2),
    total_assets decimal(15,2)

    
);
-- =====================================================
-- table: cashflow
-- =====================================================

create table cashflow (
    id int primary key,
  company_id VARCHAR(20) NOT NULL,
    year VARCHAR(20),

    operating_activity decimal(15,2),
    investing_activity decimal(15,2),
    financing_activity decimal(15,2),
    net_cash_flow decimal(15,2)

    
);
-- =====================================================
-- table: profitandloss
-- =====================================================

create table profitandloss (
    id int primary key,
    company_id VARCHAR(20) NOT NULL,
    year VARCHAR(20),

    sales decimal(15,2),
    expenses decimal(15,2),
    operating_profit decimal(15,2),
    opm_percentage decimal(10,2),
    other_income decimal(15,2),
    interest decimal(15,2),
    depreciation decimal(15,2),
    profit_before_tax decimal(15,2),
    tax_percentage decimal(10,2),
    net_profit decimal(15,2),
    eps decimal(10,2),
    dividend_payout decimal(10,2)

    
);
-- =====================================================
-- table: financial_ratio
-- =====================================================

create table financial_ratio (
    id int primary key,
    company_id VARCHAR(20) NOT NULL,
    year VARCHAR(20),
    net_profit_margin_pct decimal(10,2),
    operating_profit_margin_pct decimal(10,2),
    return_on_equity_pct decimal(10,2),
    debt_to_equity decimal(10,2),
    interest_coverage decimal(10,2),
    asset_turnover decimal(10,2),
    free_cash_flow_cr decimal(15,2),
    capex_cr decimal(15,2),
    earnings_per_share decimal(10,2),
    book_value_per_share decimal(10,2),
    dividend_payout_ratio_pct decimal(10,2),
    total_debt_cr decimal(15,2),
    cash_from_operations_cr decimal(15,2)

);
-- =====================================================
-- table: market_cap
-- =====================================================

create table market_cap (
    id int primary key,
    company_id VARCHAR(20) NOT NULL,
    year VARCHAR(20),

    market_cap_crore decimal(15,2),
    enterprise_value_crore decimal(15,2),
    pe_ratio decimal(10,2),
    pb_ratio decimal(10,2),
    ev_ebitda decimal(10,2),
    dividend_yield_pct decimal(10,2)

    
);
-- =====================================================
-- table: sectors
-- =====================================================

create table sectors (
    id int primary key,
    company_id VARCHAR(20) NOT NULL,

    broad_sector varchar(100),
    sub_sector varchar(150),
    index_weight_pct decimal(10,2),
    market_cap_category varchar(50)

   
);
-- =====================================================
-- table: stock_prices
-- =====================================================

create table stock_prices (
    id int primary key,
    company_id VARCHAR(20) NOT NULL,
    date date,

    open_price decimal(15,2),
    high_price decimal(15,2),
    low_price decimal(15,2),
    close_price decimal(15,2),
    volume bigint,
    adjusted_close decimal(15,2)

   
);
-- =====================================================
-- table: documents
-- =====================================================

create table documents (
    id int primary key,
    company_id VARCHAR(20) NOT NULL,
   year VARCHAR(20),

    annual_report text

    
);
-- =====================================================
-- table: peer_groups
-- =====================================================

create table peer_groups (
    id int primary key,
    peer_group_name varchar(150) not null,
    company_id VARCHAR(20) NOT NULL,
    is_benchmark boolean

    
);
-- =====================================================
-- table: prosandcons
-- =====================================================

create table prosandcons (
    id int primary key,
    company_id VARCHAR(20) NOT NULL,

    pros text,
    cons text

    
);
-- =====================================================
-- table: analysis
-- =====================================================

create table analysis (
    id int primary key,
    company_id VARCHAR(20),

    compounded_sales_growth decimal(10,2),
    compounded_profit_growth decimal(10,2),
    stock_price_cagr decimal(10,2),
    roe decimal(10,2)
);
