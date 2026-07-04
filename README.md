# Nifty100 Financial Intelligence Platform

## Project Overview

The Nifty100 Financial Intelligence Platform is a data engineering project that ingests, validates, and stores financial data for Nifty 100 companies.

The project loads data from multiple Excel datasets into a MySQL database, performs data validation checks, and provides analytical SQL queries for financial analysis and exploration.

## Technologies Used

* Python
* Pandas
* MySQL
* SQLAlchemy
* PyMySQL
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

## Author

Karan Taynak
