"""
Sprint 2 - Day 11
Cash Flow KPI Engine
"""


def free_cash_flow(
        operating_activity,
        investing_activity):
    return operating_activity + investing_activity


def cfo_quality_score(
        cfo,
        pat):
    """
    CFO/PAT Ratio
    """

    if pat == 0:
        return None

    ratio = cfo / pat

    if ratio > 1:
        return "High Quality"

    if ratio >= 0.5:
        return "Moderate"

    return "Accrual Risk"


def capex_intensity(
        investing_activity,
        sales):
    """
    abs(CFI) / Sales
    """

    if sales == 0:
        return None

    value = (
        abs(investing_activity) / sales
    ) * 100

    if value < 3:
        return "Asset Light"

    if value <= 8:
        return "Moderate"

    return "Capital Intensive"


def fcf_conversion_rate(
        free_cash_flow,
        operating_profit):
    if operating_profit == 0:
        return None

    return round(
        (free_cash_flow / operating_profit)
        * 100,
        2
    )


def capital_allocation_pattern(
        cfo,
        cfi,
        cff,
        quality=None):
    """
    8-pattern classifier
    """

    signs = (
        "+" if cfo >= 0 else "-",
        "+" if cfi >= 0 else "-",
        "+" if cff >= 0 else "-"
    )

    pattern = "".join(signs)

    mapping = {
        "+--": "Reinvestor",
        "++-": "Liquidating Assets",
        "-++": "Distress Signal",
        "--+": "Growth Funded by Debt",
        "+++": "Cash Accumulator",
        "---": "Pre-Revenue",
        "+-+": "Mixed"
    }

    if (
        pattern == "+--"
        and quality == "High Quality"
    ):
        return "Shareholder Returns"

    return mapping.get(
        pattern,
        "Unknown"
    )