# 📊 Nifty100 Financial Intelligence Platform

A comprehensive Financial Intelligence Platform built using **Python, FastAPI, Streamlit, MySQL, and SQLAlchemy** for analyzing Nifty 100 companies. The platform combines ETL pipelines, financial KPI calculations, REST APIs, and an interactive dashboard to help investors and analysts make data-driven decisions.

---

# Features

- Financial data ETL pipeline
- Company financial profile
- Balance Sheet analysis
- Profit & Loss analysis
- Cash Flow analysis
- Financial KPI engine
- Investment Screener
- Sector-wise analytics
- Peer comparison
- Market capitalization analysis
- Portfolio statistics
- Annual report/document retrieval
- FastAPI REST APIs
- Streamlit dashboard
- OpenAPI documentation
- Postman collection
- Automated testing with Pytest
- Performance testing

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

# Project Structure

```text
Nifty100_Financial_Intelligence_Platform/

├── config/
├── data/
├── docs/
├── mysql/
├── notebooks/
├── output/
├── reports/
├── src/
│   ├── api/
│   ├── analytics/
│   ├── dashboard/
│   ├── etl/
│   ├── schemas/
│   ├── services/
│   └── screener/
├── tests/
└── README.md
```

---

# Installation

Clone the repository

```bash
git clone <repository-url>
```

Move into the project

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

The ETL pipeline:

- Loads source datasets
- Cleans financial data
- Normalizes values
- Calculates KPIs
- Loads data into the database

---

# Starting the API

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

# Starting the Dashboard

```bash
streamlit run src/dashboard/app.py
```

Dashboard URL

```
http://localhost:8501
```

---

# Running Tests

Execute all tests

```bash
python -m pytest tests -v
```

Generate HTML report

```bash
python -m pytest tests --html=reports/pytest_report.html
```

---

# Major API Endpoints

| Endpoint | Description |
|-----------|-------------|
| `/api/v1/health` | Application health |
| `/api/v1/companies` | Company list |
| `/api/v1/companies/{ticker}` | Company profile |
| `/api/v1/screener` | Financial screener |
| `/api/v1/sectors` | Sector summary |
| `/api/v1/sectors/{sector}/companies` | Companies by sector |
| `/api/v1/peers/{group}` | Peer comparison |
| `/api/v1/market-cap/{ticker}` | Market cap history |
| `/api/v1/portfolio/stats` | Portfolio statistics |
| `/api/v1/companies/{ticker}/documents` | Annual reports |

---

# Testing

The project includes automated testing for:

- ETL
- Data Quality
- KPI Calculations
- REST APIs
- Performance Testing
- Integration Testing

Current Status

- **108 automated tests passing**
- HTML test report generated
- API integration verified

---

# Performance

Completed performance validation:

- 10 concurrent API requests
- Total execution time: **3.06 seconds**
- API response target achieved
- SQLite query optimization applied

---

# Documentation

Project documentation includes:

- Analyst Guide
- OpenAPI Specification
- Postman Collection
- Performance Notes
- HTML Test Report

---

# Future Improvements

- Authentication and authorization
- Portfolio management
- Live stock market integration
- Advanced charting
- Watchlists
- AI-powered financial insights

---

# Author

**Karan Taynak**

BBA (Hons) | Python | SQL | FastAPI | Streamlit | Data Analytics

---

# License

This project was developed for educational and portfolio purposes.