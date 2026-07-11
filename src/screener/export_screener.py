import os
import pandas as pd

from engine import (
    load_config,
    load_financial_ratios,
    apply_filters
)


def export_screeners():

    os.makedirs("output", exist_ok=True)

    config = load_config()

    df = load_financial_ratios()

    presets = [
        "quality_compounder",
        "value_pick",
        "growth_accelerator",
        "dividend_champion",
        "debt_free_blue_chip",
        "turnaround_watch"
    ]

    output_file = "output/screener_output.xlsx"

    with pd.ExcelWriter(
        output_file,
        engine="openpyxl"
    ) as writer:

        for preset in presets:

            print(f"\nRunning {preset}...")

            result = apply_filters(
                df.copy(),
                config[preset]
            )

            result = result.sort_values(
                by="composite_quality_score",
                ascending=False
            )

            result.to_excel(
                writer,
                sheet_name=preset[:31],
                index=False
            )

            print(
                f"{len(result)} companies exported."
            )

    print("\n========================================")
    print("Screener export completed successfully.")
    print(f"File saved to: {output_file}")
    print("========================================")


if __name__ == "__main__":

    export_screeners()