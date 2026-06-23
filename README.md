# Nifty100 Financial Intelligence Platform

## Project Overview

The Nifty100 Financial Intelligence Platform is a data engineering project that ingests, validates, and stores financial data for Nifty100 companies.

The project loads data from 12 source Excel files into MySQL, performs validation checks, and provides analytical SQL queries for exploration.

## Technologies Used

* Python
* Pandas
* MySQL
* SQLAlchemy
* PyMySQL
* VS Code

## Database Tables

1. companies
2. balancesheet
3. cashflow
4. profitandloss
5. financial_ratio
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

| Table           | Rows |
| --------------- | ---- |
| companies       | 92   |
| balancesheet    | 1312 |
| cashflow        | 1187 |
| profitandloss   | 1276 |
| financial_ratio | 1184 |
| market_cap      | 552  |
| sectors         | 92   |
| stock_prices    | 5520 |
| documents       | 1585 |
| peer_groups     | 56   |
| prosandcons     | 16   |
| analysis        | 20   |

## Deliverables

* Database schema
* ETL scripts
* Validation reports
* Audit reports
* SQL queries
* Unit tests

## Sprint 1 Completion Summary

### Database
- MySQL database created
- 12 tables populated
- Data successfully loaded

### Row Counts
- Companies: 92
- Balance Sheet: 1312
- Cash Flow: 1187
- Profit & Loss: 1276
- Financial Ratios: 1184
- Market Cap: 552
- Stock Prices: 5520
- Documents: 1585
- Peer Groups: 56
- Pros & Cons: 16
- Analysis: 20
- Sectors: 92

### Deliverables
- ETL Pipeline
- SQL Schema
- Load Audit Report
- Validation Report
- Exploratory Queries
- Unit Test Structure

## Author

Karan Taynak
