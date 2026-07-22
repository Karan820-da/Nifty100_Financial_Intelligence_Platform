from src.reports.data_loader import (
    load_company,
    load_profit_loss,
    load_ratios,
    load_balance_sheet,
    load_market_cap,
)

import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = A4


# --------------------------------------------------
# Header
# --------------------------------------------------
def draw_header(c, company_name, ticker):

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

    c.setFont("Helvetica-Bold", 20)
    c.drawString(
        40,
        PAGE_HEIGHT - 30,
        company_name,
    )

    c.setFont("Helvetica", 12)
    c.drawString(
        40,
        PAGE_HEIGHT - 48,
        ticker,
    )


# --------------------------------------------------
# KPI Tile
# --------------------------------------------------
def draw_kpi_tile(c, x, y, width, height, title, value):

    c.setFillColor(colors.whitesmoke)
    c.setStrokeColor(colors.grey)

    c.roundRect(
        x,
        y,
        width,
        height,
        8,
        fill=1,
    )

    c.setFillColor(colors.black)

    c.setFont("Helvetica", 10)
    c.drawString(
        x + 10,
        y + height - 18,
        title,
    )

    c.setFont("Helvetica-Bold", 16)
    c.drawString(
        x + 10,
        y + 18,
        value,
    )


# --------------------------------------------------
# Placeholder
# --------------------------------------------------
def draw_placeholder(c, x, y, width, height, title):

    c.setStrokeColor(colors.lightgrey)

    c.rect(
        x,
        y,
        width,
        height,
    )

    c.setFillColor(colors.grey)

    c.setFont("Helvetica", 12)

    c.drawCentredString(
        x + width / 2,
        y + height / 2,
        title,
    )


# --------------------------------------------------
# Create PDF
# --------------------------------------------------
def create_tearsheet(company_id):

    company = load_company(company_id)
    profit_loss = load_profit_loss(company_id)
    ratios = load_ratios(company_id)
    balance_sheet = load_balance_sheet(company_id)
    market_cap = load_market_cap(company_id)

    company_name = company.iloc[0]["company_name"]
    ticker = company.iloc[0]["id"]

    latest_ratio = ratios.iloc[-1]
    latest_market = market_cap.iloc[0]

    market_cap_value = f"₹{latest_market['market_cap_crore']:,.0f} Cr"
    pe_ratio = f"{latest_market['pe_ratio']:.2f}"
    roe = f"{company.iloc[0]['roe_percentage'] * 100:.2f}%"
    roce = f"{company.iloc[0]['roce_percentage']:.2f}%"
    eps = f"₹{latest_ratio['earnings_per_share']:.2f}"
    dividend = f"{latest_ratio['dividend_payout_ratio_pct']:.2f}%"

    os.makedirs("reports/tearsheets", exist_ok=True)

   


    pdf_path = os.path.join(
        "reports",
        "tearsheets",
        f"{company_id}_tearsheet.pdf",
    )

    c = canvas.Canvas(
        pdf_path,
        pagesize=A4,
    )

    # ----------------------------------------
    # Header
    # ----------------------------------------

    draw_header(
    c,
    company_name,
    ticker,
    )

    # ----------------------------------------
    # KPI Tiles
    # ----------------------------------------

    start_x = 40
    start_y = 610

    tile_width = 155
    tile_height = 70

    gap = 15

    kpis = [
    ("Market Cap", market_cap_value),
    ("PE Ratio", pe_ratio),
    ("ROE", roe),
    ("ROCE", roce),
    ("EPS", eps),
    ("Dividend", dividend),
]

    for i, (title, value) in enumerate(kpis):

        row = i // 3
        col = i % 3

        x = start_x + col * (tile_width + gap)
        y = start_y - row * (tile_height + gap)

        draw_kpi_tile(
            c,
            x,
            y,
            tile_width,
            tile_height,
            title,
            value,
        )

    # ----------------------------------------
    # Revenue Chart Placeholder
    # ----------------------------------------

    draw_placeholder(
        c,
        40,
        320,
        240,
        170,
        "Revenue Chart",
    )

    # ----------------------------------------
    # Profit Chart Placeholder
    # ----------------------------------------

    draw_placeholder(
        c,
        315,
        320,
        240,
        170,
        "Net Profit Chart",
    )

    # ----------------------------------------
    # ROE Placeholder
    # ----------------------------------------

    draw_placeholder(
        c,
        40,
        80,
        515,
        180,
        "ROE vs ROCE",
    )

    c.save()

    print("=" * 50)
    print("PDF CREATED SUCCESSFULLY")
    print(pdf_path)
    print("=" * 50)


if __name__ == "__main__":
    create_tearsheet("TCS")

