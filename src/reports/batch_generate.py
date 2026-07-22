import os
import pandas as pd

from src.dashboard.utils.db import get_engine
from src.reports.tearsheet import create_tearsheet

engine = get_engine()


def get_all_companies():

    query = """
    SELECT id, company_name
    FROM companies
    ORDER BY id
    """

    return pd.read_sql(query, engine)


def generate_all_tearsheets():

    companies = get_all_companies()

    print(f"Found {len(companies)} companies")

    generated = 0
    skipped = []

    for _, row in companies.iterrows():

        company_id = row["id"]

        print(f"Generating: {company_id}")

        try:
            create_tearsheet(company_id)
            generated += 1

        except Exception as e:
            print(f"Skipping {company_id}: {e}")

            skipped.append({
                "company_id": company_id,
                "reason": str(e)
            })

    os.makedirs("output", exist_ok=True)

    pd.DataFrame(skipped).to_csv(
        "output/skipped_tearsheets.csv",
        index=False
    )

    print("=" * 50)
    print(f"Generated {generated} tearsheets")
    print(f"Skipped   {len(skipped)} tearsheets")
    print("Skipped log saved to output/skipped_tearsheets.csv")
    print("=" * 50)


if __name__ == "__main__":
    generate_all_tearsheets()