# Valuation Analytics Report

## Project

Nifty100 Financial Intelligence Platform

---

## Objective

The Valuation Analytics module helps investors evaluate whether a company appears fairly valued, undervalued, or overvalued relative to its sector using key financial metrics.

---

## Data Sources

- Companies
- Financial Ratios
- Market Capitalization
- Sector Information

Database: MySQL

---

## Valuation Metrics

### 1. Price-to-Earnings (PE) Ratio
Measures how much investors are willing to pay for ₹1 of earnings.

### 2. Price-to-Book (PB) Ratio
Compares market value with book value.

### 3. EV/EBITDA
Enterprise valuation multiple.

### 4. Free Cash Flow Yield (FCF Yield)

Formula:

FCF Yield (%) = (Free Cash Flow / Market Capitalization) × 100

Higher values generally indicate better cash generation relative to market value.

---

## Sector Comparison

Each company's PE Ratio is compared with the median PE of companies within the same sector.

### Valuation Rules

| Condition | Flag |
|-----------|------|
| PE > 150% of Sector Median | Caution |
| PE < 70% of Sector Median | Discount |
| Otherwise | Fair |
| Missing Data | No Data |

---

## Dashboard Features

- Company-wise valuation metrics
- Sector comparison
- PE Distribution
- Sector Median PE
- Valuation Flag Analysis
- Interactive filtering
- CSV Export

---

## Outputs

Generated files:

- output/valuation_summary.xlsx
- output/valuation_flags.csv

---

## Technology Stack

- Python
- Streamlit
- MySQL
- SQLAlchemy
- Pandas
- Plotly

---

## Conclusion

The Valuation Analytics module provides investors with an overview of company valuation relative to sector peers. It combines financial ratios, market capitalization, and cash flow analysis to identify potentially undervalued and overvalued companies.