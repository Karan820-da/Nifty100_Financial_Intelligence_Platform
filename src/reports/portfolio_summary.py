from src.reports.data_loader import (
    load_company,
    load_profit_loss,
    load_ratios,
    load_market_cap,
)

from src.dashboard.utils.db import get_engine

import os
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = A4

engine = get_engine()

# --------------------------------------------------
# Load Sector
# --------------------------------------------------

def load_sector(company_id):

    query = f"""
        SELECT broad_sector
        FROM sectors
        WHERE company_id = '{company_id}'
        LIMIT 1
    """

    return pd.read_sql(query, engine)

# --------------------------------------------------
# Load All Companies
# --------------------------------------------------

def get_all_companies():

    query = """
        SELECT
            id,
            company_name
        FROM companies
        ORDER BY id
    """

    return pd.read_sql(query, engine)


# --------------------------------------------------
# Display Company Data
# --------------------------------------------------

def display_company_summary(company_id):

    company = load_company(company_id)
    ratios = load_ratios(company_id)
    market = load_market_cap(company_id)
    sector = load_sector(company_id)

    latest_ratio = ratios.iloc[-1]
    latest_market = market.iloc[0]

# --------------------------------------------------
# Header
# --------------------------------------------------

def draw_header(c):

    header_height = 60

    c.setFillColor(colors.darkblue)

    c.rect(
        0,
        PAGE_HEIGHT - header_height,
        PAGE_WIDTH,
        header_height,
        fill=1,
        stroke=0,
    )

    c.setFillColor(colors.white)

    c.setFont("Helvetica-Bold", 18)

    c.drawString(
        40,
        PAGE_HEIGHT - 28,
        "NIFTY100 FINANCIAL INTELLIGENCE PLATFORM",
    )

    c.setFont("Helvetica", 11)

    c.drawString(
        40,
        PAGE_HEIGHT - 46,
        "Portfolio Summary",
    )

# --------------------------------------------------
# Company Information
# --------------------------------------------------

def draw_company_info(c, company_name, ticker, sector):

    start_y = 730

    c.setFillColor(colors.black)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, start_y, company_name)

    c.setFont("Helvetica", 11)

    c.drawString(
        40,
        start_y - 25,
        f"Ticker : {ticker}",
    )

    c.drawString(
        220,
        start_y - 25,
        f"Sector : {sector}",
    )

# --------------------------------------------------
# KPI Table
# --------------------------------------------------

def draw_kpi_table(c, kpis):

    x = 40
    y = 640

    row_height = 32
    table_width = 515

    c.setStrokeColor(colors.grey)

    for title, value in kpis:

        c.rect(
            x,
            y,
            table_width,
            row_height,
            stroke=1,
            fill=0,
        )

        c.setFont("Helvetica", 11)

        c.drawString(
            x + 10,
            y + 10,
            title,
        )

        c.setFont("Helvetica-Bold", 11)

        c.drawRightString(
            x + table_width - 10,
            y + 10,
            value,
        )

        y -= row_height

# --------------------------------------------------
# Trend Arrow
# --------------------------------------------------

def get_trend_arrow(previous, current):

    if previous == 0:
        return "→"

    change = ((current - previous) / previous) * 100

    if change > 2:
        return "↑"

    elif change < -2:
        return "↓"

    return "→"

# --------------------------------------------------
# Trend Section
# --------------------------------------------------

def draw_trend_section(c, revenue_arrow, profit_arrow, eps_arrow):

    x = 40
    y = 360

    c.setFont("Helvetica-Bold", 13)
    c.drawString(x, y, "Business Trends")

    c.line(x, y - 8, 555, y - 8)

    rows = [

        ("Revenue", revenue_arrow),

        ("Net Profit", profit_arrow),

        ("EPS", eps_arrow),

    ]

    y -= 40

    for metric, arrow in rows:

        c.setFont("Helvetica", 11)
        c.drawString(x + 10, y, metric)

        c.setFont("Helvetica-Bold", 16)
        c.drawRightString(535, y, arrow)

        y -= 30


def create_portfolio_summary(company_id):

    company = load_company(company_id)
    ratios = load_ratios(company_id)
    market = load_market_cap(company_id)
    sector = load_sector(company_id)

    latest_ratio = ratios.iloc[-1]
    latest_market = market.iloc[0]

    company_name = company.iloc[0]["company_name"]
    ticker = company.iloc[0]["id"]

    market_cap = f"INR {latest_market['market_cap_crore']:,.0f} Cr"
    pe = f"{latest_market['pe_ratio']:.2f}"
    roe = f"{company.iloc[0]['roe_percentage'] * 100:.2f}%"
    roce = f"{company.iloc[0]['roce_percentage']:.2f}%"
    eps = f"INR {latest_ratio['earnings_per_share']:.2f}"
    dividend = f"{latest_ratio['dividend_payout_ratio_pct']:.2f}%"

    kpis = [
        ("Market Cap", market_cap),
        ("PE Ratio", pe),
        ("ROE", roe),
        ("ROCE", roce),
        ("EPS", eps),
        ("Dividend", dividend),
    ]

    os.makedirs("reports/portfolio", exist_ok=True)

    pdf_path = os.path.join(
        "reports",
        "portfolio",
        "portfolio_summary.pdf",
    )

    c = canvas.Canvas(pdf_path, pagesize=A4)

    draw_header(c)

    draw_company_info(
        c,
        company_name,
        ticker,
        sector.iloc[0]["broad_sector"],
    )

    draw_kpi_table(c, kpis)

    draw_trend_section(
        c,
        "↑",
        "↑",
        "↑",
    )

    c.save()

    print("=" * 50)
    print("PORTFOLIO SUMMARY CREATED")
    print(pdf_path)
    print("=" * 50)

def create_portfolio_summary_all():

    companies = get_all_companies()

    os.makedirs(
        "reports/portfolio",
        exist_ok=True,
    )

    pdf_path = os.path.join(
        "reports",
        "portfolio",
        "portfolio_summary.pdf",
    )

    c = canvas.Canvas(
        pdf_path,
        pagesize=A4,
    )

    total_companies = 0

    for _, row in companies.iterrows():

        company_id = row["id"]

        try:

            # ----------------------------
            # Load Data
            # ----------------------------

            company = load_company(company_id)
            profit = load_profit_loss(company_id)
            ratios = load_ratios(company_id)
            market = load_market_cap(company_id)
            sector = load_sector(company_id)

            # ----------------------------
            # Trend Calculation
            # ----------------------------

            annual_profit = profit[
                profit["year"] != "TTM"
            ].copy()

            if len(annual_profit) >= 2:

                previous_year = annual_profit.iloc[-2]
                latest_year = annual_profit.iloc[-1]

                revenue_arrow = get_trend_arrow(
                    previous_year["sales"],
                    latest_year["sales"],
                )

                profit_arrow = get_trend_arrow(
                    previous_year["net_profit"],
                    latest_year["net_profit"],
                )

                eps_arrow = get_trend_arrow(
                    previous_year["eps"],
                    latest_year["eps"],
                )

            else:

                revenue_arrow = "→"
                profit_arrow = "→"
                eps_arrow = "→"

            # ----------------------------
            # Latest Values
            # ----------------------------

            latest_ratio = ratios.iloc[-1]
            latest_market = market.iloc[0]

            company_name = company.iloc[0]["company_name"]
            ticker = company.iloc[0]["id"]

            market_cap = f"INR {latest_market['market_cap_crore']:,.0f} Cr"
            pe = f"{latest_market['pe_ratio']:.2f}"
            roe = f"{company.iloc[0]['roe_percentage'] * 100:.2f}%"
            roce = f"{company.iloc[0]['roce_percentage']:.2f}%"
            eps = f"INR {latest_ratio['earnings_per_share']:.2f}"
            dividend = f"{latest_ratio['dividend_payout_ratio_pct']:.2f}%"

            kpis = [
                ("Market Cap", market_cap),
                ("PE Ratio", pe),
                ("ROE", roe),
                ("ROCE", roce),
                ("EPS", eps),
                ("Dividend", dividend),
            ]

            # ----------------------------
            # Draw PDF
            # ----------------------------

            draw_header(c)

            draw_company_info(
                c,
                company_name,
                ticker,
                sector.iloc[0]["broad_sector"],
            )

            draw_kpi_table(
                c,
                kpis,
            )

            draw_trend_section(
                c,
                revenue_arrow,
                profit_arrow,
                eps_arrow,
            )

            total_companies += 1

            c.showPage()

            print(f"✓ {ticker}")

        except Exception as e:

            print(f"✗ {company_id} : {e}")

    c.save()

    print("=" * 60)
    print("Portfolio Summary Created Successfully")
    print(f"Companies Added : {total_companies}")
    print(pdf_path)
    print("=" * 60)
# --------------------------------------------------
# Test
# --------------------------------------------------
if __name__ == "__main__":

    create_portfolio_summary_all()
