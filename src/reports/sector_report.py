import os
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from src.dashboard.utils.db import get_engine

engine = get_engine()
styles = getSampleStyleSheet()


# ============================================================
# Get all sectors
# ============================================================

def get_all_sectors():

    query = """
    SELECT DISTINCT broad_sector
    FROM sectors
    ORDER BY broad_sector
    """

    return pd.read_sql(query, engine)


# ============================================================
# Load companies in a sector
# ============================================================

def load_sector_companies(sector):

    query = f"""
    SELECT
        c.id,
        c.company_name,
        s.broad_sector,

        MAX(mc.market_cap_crore) AS market_cap_crore,
        MAX(mc.pe_ratio) AS pe_ratio,

        MAX(c.roe_percentage) AS roe_percentage,
        MAX(c.roce_percentage) AS roce_percentage,

        MAX(fr.earnings_per_share) AS earnings_per_share,
        MAX(fr.dividend_payout_ratio_pct) AS dividend_payout_ratio_pct

    FROM companies c

    JOIN sectors s
        ON c.id = s.company_id

    LEFT JOIN market_cap mc
        ON c.id = mc.company_id

    LEFT JOIN financial_ratios fr
        ON c.id = fr.company_id

    WHERE s.broad_sector = '{sector}'

    GROUP BY
        c.id,
        c.company_name,
        s.broad_sector

    ORDER BY c.company_name;
    """

    return pd.read_sql(query, engine)


# ============================================================
# Create Sector Report PDF
# ============================================================

def create_sector_report(sector):

    df = load_sector_companies(sector)

    if df.empty:
        print(f"No companies found for {sector}")
        return

    os.makedirs("reports/sector", exist_ok=True)

    pdf_path = f"reports/sector/{sector}_report.pdf"

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30,
    )

    story = []

    # --------------------------------------------------------
    # Title
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "<b>NIFTY100 FINANCIAL INTELLIGENCE PLATFORM</b>",
            styles["Title"],
        )
    )

    story.append(
        Paragraph(
            f"<b>{sector} Sector Report</b>",
            styles["Heading1"],
        )
    )

    story.append(Spacer(1, 0.30 * inch))

    # --------------------------------------------------------
    # Calculate Summary
    # --------------------------------------------------------

    median_market_cap = df["market_cap_crore"].median(skipna=True)
    median_pe = df["pe_ratio"].median(skipna=True)
    median_roe = df["roe_percentage"].median(skipna=True)
    median_roce = df["roce_percentage"].median(skipna=True)
    median_eps = df["earnings_per_share"].median(skipna=True)
    median_dividend = df["dividend_payout_ratio_pct"].median(skipna=True)

    summary_data = [
        ["Metric", "Value"],
        ["Total Companies", len(df)],
        ["Median Market Cap", "-" if pd.isna(median_market_cap) else f"{median_market_cap:,.2f}"],
        ["Median PE", "-" if pd.isna(median_pe) else f"{median_pe:.2f}"],
        ["Median ROE", "-" if pd.isna(median_roe) else f"{median_roe:.2f}%"],
        ["Median ROCE", "-" if pd.isna(median_roce) else f"{median_roce:.2f}%"],
        ["Median EPS", "-" if pd.isna(median_eps) else f"{median_eps:.2f}"],
        ["Median Dividend", "-" if pd.isna(median_dividend) else f"{median_dividend:.2f}%"],
    ]

    summary_table = Table(summary_data, colWidths=[3.5 * inch, 2 * inch])

    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
            ]
        )
    )

    story.append(summary_table)

    story.append(Spacer(1, 0.40 * inch))

    # --------------------------------------------------------
    # Company Table
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "<b>Companies</b>",
            styles["Heading2"],
        )
    )

    table_data = [[
        "Company",
        "PE",
        "ROE",
        "ROCE",
        "EPS",
        "Dividend"
    ]]

    for _, row in df.iterrows():

        company = str(row["company_name"]).replace("\n", "").strip()

        pe = "-" if pd.isna(row["pe_ratio"]) else f"{row['pe_ratio']:.2f}"
        roe = "-" if pd.isna(row["roe_percentage"]) else f"{row['roe_percentage']:.2f}"
        roce = "-" if pd.isna(row["roce_percentage"]) else f"{row['roce_percentage']:.2f}"
        eps = "-" if pd.isna(row["earnings_per_share"]) else f"{row['earnings_per_share']:.2f}"
        dividend = "-" if pd.isna(row["dividend_payout_ratio_pct"]) else f"{row['dividend_payout_ratio_pct']:.2f}"

        table_data.append([
            company,
            pe,
            roe,
            roce,
            eps,
            dividend,
        ])

    company_table = Table(
        table_data,
        colWidths=[
            3.3 * inch,
            0.7 * inch,
            0.8 * inch,
            0.8 * inch,
            0.8 * inch,
            0.9 * inch,
        ],
    )

    company_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
            ]
        )
    )

    story.append(company_table)

    doc.build(story)

    print("=" * 60)
    print(f"Sector Report Created Successfully")
    print(pdf_path)
    print("=" * 60)


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    sectors = get_all_sectors()

    generated = 0
    skipped = []

    print("=" * 60)
    print("Generating Sector Reports")
    print("=" * 60)

    for sector in sectors["broad_sector"]:

        print(f"\nGenerating: {sector}")

        try:

            create_sector_report(sector)
            generated += 1

        except Exception as e:

            print(f"Skipping {sector}: {e}")

            skipped.append({
                "sector": sector,
                "reason": str(e)
            })

    print("\n" + "=" * 60)
    print(f"Generated : {generated}")
    print(f"Skipped  : {len(skipped)}")

    if skipped:
        print("\nSkipped Sectors:")

        for item in skipped:
            print(f"- {item['sector']} : {item['reason']}")

    print("=" * 60)

