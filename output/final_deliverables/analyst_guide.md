# Nifty100 Financial Intelligence Platform
## Analyst Guide

**Version:** 1.0

**Author:** Karan Taynak

---

# Table of Contents

1. Introduction
2. Project Overview
3. System Architecture
4. Dashboard Overview
5. Company Profile
6. Financial Screener
7. Sector Analysis
8. Peer Comparison
9. API Usage
10. PDF Tearsheet Generation
11. Troubleshooting
12. Frequently Asked Questions

---

# 1. Introduction

The Nifty100 Financial Intelligence Platform is an analytics platform designed to help analysts, investors, and researchers explore financial data for Nifty 100 companies.

The platform combines:

- FastAPI REST APIs
- Streamlit Dashboard
- MySQL Database
- ETL Pipelines
- Financial KPI Engine
- Automated Testing

It provides company financial statements, valuation metrics, screening capabilities, peer comparison, sector analysis, and downloadable reports.

---

# 2. Project Overview

The platform consists of four major components.

## ETL Layer

Responsible for:

- Loading Excel data
- Cleaning datasets
- Standardizing financial fields
- Calculating KPIs
- Loading records into MySQL

---

## Database

Stores:

- Companies
- Balance Sheets
- Cash Flow Statements
- Profit & Loss
- Financial Ratios
- Market Capitalization
- Sector Classification
- Peer Groups
- Documents

---

## API Layer

Built using FastAPI.

Provides REST endpoints for:

- Companies
- Screener
- Sectors
- Peers
- Portfolio Statistics
- Market Cap
- Documents
- Health Monitoring

---

## Dashboard

Built using Streamlit.

Allows users to explore financial data interactively.

---

# 3. System Architecture

Data Flow

Excel Files

↓

ETL Pipeline

↓

MySQL Database

↓

FastAPI

↓

Streamlit Dashboard

↓

End User

---

# 4. Dashboard Overview

The dashboard contains several modules.

### Company Profile

Displays:

- Company information
- ROE
- ROCE
- Book Value
- Market Cap
- Financial Ratios

---

### Financial Statements

Users can view:

- Balance Sheet
- Profit & Loss
- Cash Flow

---

### Screener

Allows filtering companies using:

- Minimum ROE
- Maximum Debt to Equity
- Maximum PE Ratio
- Minimum Market Capitalization

Results are updated instantly.

---

### Sector Analysis

Shows:

- Sector summary
- Company count
- Median ROE
- Median PE
- Median Debt to Equity

---

### Peer Comparison

Compare companies within peer groups.

Includes:

- Percentile Ranking
- Financial KPIs
- Benchmark Company

---

# 5. Company Profile

The Company Profile page provides a consolidated overview of an individual company's financial information.

## Features

The screen displays:

- Company Name
- Company Logo
- Sector and Sub-Sector
- Company Description
- Official Website
- NSE and BSE Profile Links
- Face Value
- Book Value
- ROE
- ROCE

Latest financial KPIs are also displayed, including:

- Net Profit Margin
- Operating Profit Margin
- Return on Equity
- Debt to Equity
- Interest Coverage
- Asset Turnover
- Free Cash Flow
- Earnings Per Share
- Revenue CAGR (5 Year)
- PAT CAGR (5 Year)

Users can quickly understand the financial health of a company without navigating multiple screens.

---

# 6. Using the Financial Screener

The Financial Screener allows analysts to filter companies based on investment criteria.

## Available Filters

- Minimum Return on Equity (ROE)
- Maximum Debt-to-Equity Ratio
- Maximum Price-to-Earnings Ratio (PE)
- Minimum Market Capitalization

Example:

An investor looking for high-quality companies may use:

- ROE ≥ 15%
- Debt-to-Equity ≤ 1
- PE ≤ 30
- Market Cap ≥ 1000 Crore

The screener immediately returns only companies satisfying all selected criteria.

## Typical Use Cases

### Value Investing

Filter companies with:

- Low PE
- Low Debt
- Positive Free Cash Flow

### Growth Investing

Filter companies with:

- High Revenue CAGR
- High PAT CAGR
- Strong ROE

### Quality Investing

Filter companies with:

- High ROE
- High Interest Coverage
- Positive Cash Flow

---

# 7. Sector Analysis

Sector Analysis groups companies according to their primary business sector.

Each sector summary includes:

- Number of Companies
- Median ROE
- Median PE Ratio
- Median Debt-to-Equity Ratio

Selecting a sector displays all companies belonging to that sector together with their latest financial KPIs.

This enables quick comparison between companies operating in the same industry.

---

# 8. Peer Comparison

Peer Comparison helps evaluate companies against their closest competitors.

Each peer group contains:

- Benchmark Company
- Peer Companies
- Percentile Rankings
- Financial Metrics

Example metrics include:

- ROE
- PE Ratio
- Debt-to-Equity
- Earnings Per Share
- Revenue CAGR
- PAT CAGR
- Asset Turnover
- Interest Coverage

The comparison assists analysts in identifying industry leaders and lagging companies.

---

# 9. API Usage

The platform exposes REST APIs using FastAPI.

The interactive API documentation is available at:

```
http://127.0.0.1:8000/docs
```

The OpenAPI specification is available at:

```
http://127.0.0.1:8000/openapi.json
```

## Example API Calls

### Health Check

```bash
curl http://127.0.0.1:8000/api/v1/health
```

### Get All Companies

```bash
curl http://127.0.0.1:8000/api/v1/companies
```

### Get Company Details

```bash
curl http://127.0.0.1:8000/api/v1/companies/TCS
```

### Financial Screener

```bash
curl "http://127.0.0.1:8000/api/v1/screener?min_roe=15&max_de=1&max_pe=30"
```

### Sector Summary

```bash
curl http://127.0.0.1:8000/api/v1/sectors
```

### Companies in IT Sector

```bash
curl http://127.0.0.1:8000/api/v1/sectors/IT/companies
```

### Company Documents

```bash
curl http://127.0.0.1:8000/api/v1/companies/TCS/documents
```

The API responses are returned in JSON format and can be consumed by web applications, dashboards, or external systems.

---

# 10. PDF Tearsheet Generation

The platform allows users to generate company-specific reports (tearsheets) that summarize key financial information.

## Typical Contents

Each tearsheet includes:

- Company Overview
- Sector Information
- Financial Ratios
- Profit & Loss Summary
- Balance Sheet Summary
- Cash Flow Summary
- Market Capitalization
- Growth Metrics
- Valuation Metrics
- Annual Report Links

These reports are intended for investment analysis and can be shared with stakeholders or saved for future reference.

---

# 11. Running the Project

## Run the ETL Pipeline

```bash
python run_pipeline.py
```

---

## Start the FastAPI Server

```bash
uvicorn src.api.main:app --reload
```

API Documentation:

```
http://127.0.0.1:8000/docs
```

---

## Start the Streamlit Dashboard

```bash
streamlit run src/dashboard/app.py
```

Dashboard URL:

```
http://localhost:8501
```

---

## Run the Test Suite

```bash
python -m pytest tests -v
```

Generate HTML report:

```bash
python -m pytest tests --html=reports/pytest_report.html
```

---

# 12. Troubleshooting

## API Does Not Start

Possible causes:

- Missing Python dependencies
- Database connection failure
- Incorrect project directory

Recommended actions:

- Install requirements
- Verify database configuration
- Restart FastAPI

---

## Dashboard Cannot Load Data

Possible causes:

- FastAPI server is not running
- Incorrect API URL
- Database unavailable

Recommended actions:

- Start FastAPI
- Verify API endpoint
- Refresh dashboard

---

## Database Errors

Possible causes:

- Missing tables
- Invalid SQL query
- Connection timeout

Recommended actions:

- Verify database schema
- Check SQL syntax
- Restart database service

---

## Tests Fail

Possible causes:

- Missing packages
- API server not running
- Database not populated

Recommended actions:

- Install required packages
- Execute ETL pipeline
- Re-run pytest

---

# Frequently Asked Questions

## Which companies are included?

The platform analyzes companies from the Nifty 100 universe available in the project dataset.

---

## Which technologies are used?

- Python
- FastAPI
- Streamlit
- MySQL
- SQLAlchemy
- Pandas
- Pytest
- Git
- GitHub

---

## Can new companies be added?

Yes.

Run the ETL pipeline with updated source data to populate the database with additional companies.

---

## Where are the API documents?

Interactive API documentation:

```
http://127.0.0.1:8000/docs
```

OpenAPI specification:

```
http://127.0.0.1:8000/openapi.json
```

---

## Where are test reports stored?

HTML reports are generated in:

```
reports/
```

Performance notes are stored in:

```
output/perf_notes.md
```

---

# Best Practices

- Run the ETL pipeline before using the dashboard.
- Keep database backups before large updates.
- Execute automated tests after code changes.
- Review API documentation before integrating external applications.
- Keep dependencies updated.
- Use Git commits with meaningful messages.

---

# Glossary

**API** — Application Programming Interface used to expose financial data.

**ETL** — Extract, Transform, Load pipeline for importing and cleaning financial data.

**ROE** — Return on Equity.

**ROCE** — Return on Capital Employed.

**PE Ratio** — Price-to-Earnings Ratio.

**Debt-to-Equity** — Financial leverage ratio.

**Market Capitalization** — Total market value of a company's outstanding shares.

**CAGR** — Compound Annual Growth Rate.

**Free Cash Flow** — Cash generated after capital expenditure.

---

# Conclusion

The Nifty100 Financial Intelligence Platform provides an integrated solution for financial data management, company analysis, screening, peer comparison, and investment research.

By combining automated ETL pipelines, a structured database, FastAPI services, Streamlit dashboards, and a comprehensive testing framework, the platform delivers reliable financial insights through an easy-to-use interface.

This guide introduced the major components of the system, explained dashboard navigation, demonstrated API usage, described common troubleshooting procedures, and outlined recommended operational practices.

Users are encouraged to keep the platform updated by refreshing data through the ETL pipeline and validating changes using the automated test suite before deployment.

---

**End of Analyst Guide**