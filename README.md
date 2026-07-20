# Nifty100 Financial Intelligence Platform

## Project Overview

The Nifty100 Financial Intelligence Platform is a data engineering project that ingests, validates, and stores financial data for Nifty 100 companies.

The project loads data from multiple Excel datasets into a MySQL database, performs data validation checks, and provides analytical SQL queries for financial analysis and exploration.

## Technologies Used

## Technologies Used

* Python
* Pandas
* NumPy
* Streamlit
* Plotly
* MySQL
* SQLAlchemy
* PyMySQL
* OpenPyXL
* VS Code
* Git & GitHub

## Database Tables

1. companies
2. balancesheet
3. cashflow
4. profitandloss
5. financial_ratios
6. market_cap
7. sectors
8. stock_prices
9. documents
10. peer_groups
11. prosandcons
12. analysis

## ETL Pipeline

* Extract data from Excel files
* Transform and normalize datasets
* Load data into MySQL database
* Perform validation checks
* Generate audit reports

## Load Summary

| Table            | Rows |
| ---------------- | ---: |
| companies        |   92 |
| balancesheet     | 1312 |
| cashflow         | 1187 |
| profitandloss    | 1276 |
| financial_ratios | 1184 |
| market_cap       |  552 |
| sectors          |   92 |
| stock_prices     | 5520 |
| documents        | 1585 |
| peer_groups      |   56 |
| prosandcons      |   16 |
| analysis         |   20 |

## Deliverables

* Database Schema
* ETL Scripts
* Validation Reports
* Audit Reports
* SQL Queries
* Unit Tests

## Sprint 1 Completion Summary

### Database

* MySQL database created
* 12 tables populated
* Data successfully loaded

### Deliverables Completed

* ETL Pipeline
* SQL Schema Design
* Data Validation
* Load Audit Report
* Exploratory SQL Queries
* Unit Test Structure
* Documentation
* GitHub Repository

## Sprint 2 Completion Summary

### Modules Implemented
- Profitability Ratios
- Leverage & Efficiency Ratios
- CAGR Engine
- Cash Flow KPI Engine
- Capital Allocation Classification
- Edge Case Logging

### Deliverables
- financial_ratios table populated with 1184 records
- output/capital_allocation.csv
- output/ratio_edge_cases.log
- 34 unit tests passing

### Key Features
- 50+ financial KPI calculations
- CAGR engine with edge case handling
- Capital allocation pattern classification
- Composite quality score calculation
- Financial anomaly detection and logging

### Sprint Status
Sprint 2 completed successfully.

## Sprint 3 – Financial Screener & Peer Analytics

### Financial Screener
- Developed a configurable financial screener using YAML-based filters.
- Implemented six preset screeners:
  - Quality Compounder
  - Value Pick
  - Growth Accelerator
  - Dividend Champion
  - Debt-Free Blue Chip
  - Turnaround Watch
- Generated `screener_output.xlsx` with filtered company results.

### CAGR Analytics
- Calculated 5-Year Revenue CAGR
- Calculated 5-Year PAT CAGR
- Calculated 5-Year EPS CAGR
- Updated CAGR values in the `financial_ratios` table.

### Composite Quality Score
- Implemented a composite quality scoring model for ranking companies.
- Used the score to rank screener results.

### Peer Analytics
- Computed peer percentile rankings across multiple financial metrics.
- Generated the `peer_percentiles` database table.

### Peer Comparison Report
- Created `peer_comparison.xlsx`.
- Generated separate worksheets for each peer group.

### Radar Charts
- Generated radar charts for all companies.
- Compared each company with its peer group.
- Saved charts in `reports/radar_charts/`.

### Testing
- Added unit tests for:
  - CAGR calculations
  - Financial ratios
  - Cash Flow KPIs
  - ETL validation
  - Screener engine

- Total Unit Tests Passed: **35**
## Sprint 4 – Valuation Analytics Dashboard

### Valuation Analytics Engine
- Developed a valuation analytics engine using financial ratios and market capitalization data.
- Integrated MySQL database with SQLAlchemy for real-time valuation analysis.
- Implemented automated valuation calculations for all supported companies.

### Valuation Metrics
- Price-to-Earnings (PE) Ratio
- Price-to-Book (PB) Ratio
- Enterprise Value to EBITDA (EV/EBITDA)
- Free Cash Flow (FCF) Yield
- Sector Median PE
- PE Premium / Discount vs Sector Median

### Valuation Classification
Implemented an automated valuation flagging system:

| Flag | Description |
|------|-------------|
| Fair | Trading close to sector median valuation |
| Discount | Trading significantly below sector median |
| Caution | Trading significantly above sector median |
| No Data | Insufficient valuation information |

### Interactive Dashboard
Added a dedicated **Valuation Dashboard** in Streamlit featuring:

- Company-wise valuation metrics
- Sector filtering
- Valuation flag filtering
- KPI summary cards
- Sector Median PE visualization
- Valuation flag distribution charts
- Interactive valuation data table
- CSV report download

### Reports Generated
- `output/valuation_summary.xlsx`
- `output/valuation_flags.csv`
- `reports/valuation_report.md`

### Dashboard Features
The platform now includes:

- Home Dashboard
- Company Profile
- Financial Screener
- Peer Comparison
- Market Trends
- Sector Analysis
- Market Capitalization Dashboard
- **Valuation Analytics Dashboard**
- Reports & Export

### Sprint 4 Deliverables
- Valuation Analytics Engine
- Free Cash Flow Yield Analysis
- Sector Median PE Analysis
- Valuation Classification Engine
- Streamlit Valuation Dashboard
- CSV & Excel Report Export
- Technical Documentation

### Sprint Status
**Sprint 4 completed successfully.**



## Author

Karan Taynak
