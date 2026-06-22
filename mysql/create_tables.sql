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

CREATE TABLE balancesheet (
    id INT PRIMARY KEY,
    company_id INT NOT NULL,

    equity_capital DECIMAL(15,2),
    reserves DECIMAL(15,2),
    borrowing DECIMAL(15,2),
    other_liabilities DECIMAL(15,2),
    fixed_assets DECIMAL(15,2),
    cwip DECIMAL(15,2),
    investments DECIMAL(15,2),
    other_asset DECIMAL(15,2),
    total_assets DECIMAL(15,2),

    FOREIGN KEY (company_id)
        REFERENCES companies(id)
);
-- =====================================================
-- table: cashflow
-- =====================================================

create table cashflow (
    id int primary key,
    company_id int not null,
    year year,

    operating_activity decimal(15,2),
    investing_activity decimal(15,2),
    financing_activity decimal(15,2),
    net_cash_flow decimal(15,2),

    foreign key (company_id)
        references companies(id)
);
-- =====================================================
-- table: profitandloss
-- =====================================================

create table profitandloss (
    id int primary key,
    company_id int not null,
    year year,

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
    dividend_payout decimal(10,2),

    foreign key (company_id)
        references companies(id)
);
-- =====================================================
-- table: financial_ratio
-- =====================================================

create table financial_ratio (
    id int primary key,
    company_id int not null,
    year year,
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
    cash_from_operations_cr decimal(15,2),

    foreign key (company_id)
        references companies(id)
);
-- =====================================================
-- table: market_cap
-- =====================================================

create table market_cap (
    id int primary key,
    company_id int not null,
    year year,

    market_cap_crore decimal(15,2),
    enterprise_value_crore decimal(15,2),
    pe_ratio decimal(10,2),
    pb_ratio decimal(10,2),
    ev_ebitda decimal(10,2),
    dividend_yield_pct decimal(10,2),

    foreign key (company_id)
        references companies(id)
);
-- =====================================================
-- table: sectors
-- =====================================================

create table sectors (
    id int primary key,
    company_id int not null,

    broad_sector varchar(100),
    sub_sector varchar(150),
    index_weight_pct decimal(10,2),
    market_cap_category varchar(50),

    foreign key (company_id)
        references companies(id)
);
-- =====================================================
-- table: stock_prices
-- =====================================================

create table stock_prices (
    id int primary key,
    company_id int not null,
    date date,

    open_price decimal(15,2),
    high_price decimal(15,2),
    low_price decimal(15,2),
    close_price decimal(15,2),
    volume bigint,
    adjusted_close decimal(15,2),

    foreign key (company_id)
        references companies(id)
);
-- =====================================================
-- table: documents
-- =====================================================

create table documents (
    id int primary key,
    company_id int not null,
    year year,

    annual_report text,

    foreign key (company_id)
        references companies(id)
);
-- =====================================================
-- table: peer_groups
-- =====================================================

create table peer_groups (
    id int primary key,
    peer_group_name varchar(150) not null,
    company_id int not null,
    is_benchmark boolean,

    foreign key (company_id)
        references companies(id)
);
-- =====================================================
-- table: prosandcons
-- =====================================================

create table prosandcons (
    id int primary key,
    company_id int not null,

    pros text,
    cons text,

    foreign key (company_id)
        references companies(id)
);
-- =====================================================
-- table: analysis
-- =====================================================

create table analysis (
    id int primary key,
    company varchar(255),

    compounded_sales_growth decimal(10,2),
    compounded_profit_growth decimal(10,2),
    stock_price_cagr decimal(10,2),
    roe decimal(10,2)
);
