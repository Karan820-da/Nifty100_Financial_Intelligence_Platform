"""
Sprint 2 - Day 10
CAGR Engine
"""


def calculate_cagr(start_value, end_value, years):
    """
    CAGR Formula:
    ((end/start)^(1/n) - 1) * 100
    """

    if years <= 0:
        return None, "INVALID_PERIOD"

    if start_value == 0:
        return None, "ZERO_BASE"

    if start_value > 0 and end_value > 0:
        cagr = (
            (end_value / start_value) ** (1 / years) - 1
        ) * 100

        return round(cagr, 2), None

    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    return None, "INSUFFICIENT"

def calculate_period_cagr(values, years):
    """
    values = ordered list of historical values
    Example:
    [100, 120, 150, 180, 200]
    """

    if len(values) < years + 1:
        return None, "INSUFFICIENT"

    start_value = values[-(years + 1)]
    end_value = values[-1]

    return calculate_cagr(
        start_value,
        end_value,
        years
    )


 