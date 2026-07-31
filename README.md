# 📊 Nifty100 Financial Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B)
![MySQL](https://img.shields.io/badge/MySQL-Database-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![Pytest](https://img.shields.io/badge/Pytest-Testing-green)
![License](https://img.shields.io/badge/License-Educational-success)

---

## Overview

The **Nifty100 Financial Intelligence Platform** is an end-to-end financial analytics application built to analyze companies in the **Nifty 100 Index**. The platform combines automated ETL pipelines, financial KPI calculations, REST APIs, and interactive dashboards to help investors, analysts, and researchers make informed, data-driven decisions.

The project follows a production-style architecture using **Python, FastAPI, Streamlit, MySQL, SQLAlchemy, and Pytest**, demonstrating backend development, data engineering, analytics, and software testing in a single application.

---

# Key Features

### 📥 Data Engineering

- Automated ETL pipeline
- Data cleaning and validation
- Financial statement processing
- Database loading
- KPI generation

### 📈 Financial Analytics

- Company Financial Profiles
- Balance Sheet Analysis
- Profit & Loss Analysis
- Cash Flow Analysis
- Financial KPI Engine
- Market Capitalization Analysis
- Sector-wise Analytics
- Peer Comparison
- Portfolio Statistics
- Investment Screener

### 🌐 Backend Development

- REST APIs built with FastAPI
- OpenAPI Documentation
- Company Search APIs
- Financial Screening APIs
- Portfolio Analytics APIs
- Document Retrieval APIs

### 📊 Dashboard

Interactive Streamlit dashboard including:

- Company Overview
- Financial Statements
- KPI Dashboard
- Sector Analytics
- Portfolio Insights
- Investment Screening

### ✅ Testing

- Automated Testing using Pytest
- ETL Validation
- API Testing
- KPI Validation
- Integration Testing
- Performance Testing

---

# Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.13 |
| Backend | FastAPI |
| Frontend | Streamlit |
| Database | MySQL |
| ORM | SQLAlchemy |
| Data Processing | Pandas |
| Testing | Pytest |
| Documentation | OpenAPI, Markdown |
| Version Control | Git & GitHub |

---

# Project Architecture

```
                 Financial Datasets
                         │
                         ▼
                 ETL Pipeline
         (Extract • Transform • Load)
                         │
                         ▼
                  MySQL Database
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
     FastAPI REST APIs          Streamlit Dashboard
          │                             │
          └──────────────┬──────────────┘
                         ▼
             Financial Intelligence Platform
```

---

# Project Structure

```
Nifty100_Financial_Intelligence_Platform/

├── config/
├── data/
│   └── raw/
├── docs/
├── mysql/
├── notebooks/
├── output/
├── reports/
├── src/
│   ├── analytics/
│   ├── api/
│   ├── dashboard/
│   ├── etl/
│   ├── schemas/
│   ├── screener/
│   └── services/
├── tests/
├── requirements.txt
├── run_pipeline.py
└── README.md
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/Karan820-da/Nifty100_Financial_Intelligence_Platform.git
```

Navigate to the project directory

```bash
cd Nifty100_Financial_Intelligence_Platform
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running the ETL Pipeline

```bash
python run_pipeline.py
```

The ETL pipeline performs:

- Data extraction
- Data cleaning
- Validation
- Transformation
- Financial KPI calculations
- Database loading

---

# Running the API

```bash
uvicorn src.api.main:app --reload
```

API Documentation

```
http://127.0.0.1:8000/docs
```

OpenAPI Specification

```
http://127.0.0.1:8000/openapi.json
```

---

# Running the Dashboard

```bash
streamlit run src/dashboard/app.py
```

Dashboard

```
http://localhost:8501
```

---

# API Endpoints

| Endpoint | Description |
|-----------|-------------|
| /api/v1/health | Application Health |
| /api/v1/companies | Company List |
| /api/v1/companies/{ticker} | Company Profile |
| /api/v1/screener | Financial Screener |
| /api/v1/sectors | Sector Analytics |
| /api/v1/sectors/{sector}/companies | Companies by Sector |
| /api/v1/peers/{group} | Peer Comparison |
| /api/v1/market-cap/{ticker} | Market Capitalization |
| /api/v1/portfolio/stats | Portfolio Statistics |
| /api/v1/companies/{ticker}/documents | Annual Reports |

---

# Automated Testing

Run all tests

```bash
python -m pytest tests -v
```

Generate HTML Report

```bash
python -m pytest tests --html=reports/pytest_report.html
```

Testing includes:

- ETL Validation
- API Testing
- KPI Calculations
- Integration Testing
- Performance Testing

---

# Project Highlights

- Developed an end-to-end Financial Intelligence Platform for **92 Nifty 100 companies**
- Built automated ETL pipelines for financial data processing
- Designed and implemented **16 REST API endpoints**
- Calculated financial KPIs including:
  - ROE
  - CAGR
  - Profit Margin
  - Debt-to-Equity Ratio
  - Interest Coverage Ratio
- Developed interactive Streamlit dashboards
- Implemented **108+ automated tests** using Pytest
- Validated API performance with concurrent requests
- Integrated MySQL database using SQLAlchemy ORM

---

# Performance

Performance validation completed with:

- 108+ automated tests passing
- API integration verified
- Concurrent API request testing
- Optimized SQL queries
- Automated HTML test reports

---

# Future Roadmap

- User Authentication
- Portfolio Management
- Live Stock Market Integration
- Advanced Interactive Charts
- Watchlists
- AI-powered Financial Insights
- Cloud Deployment

---

# Author

## Karan Taynak

**Data Analyst | Python | SQL | FastAPI | Streamlit | MySQL | Financial Analytics**

- GitHub: https://github.com/Karan820-da
- LinkedIn: https://www.linkedin.com/in/karan-taynak-47b906223/
- Email: karantaynak3777@gmail.com

---

# License

This project was developed for educational, learning, and portfolio purposes.
