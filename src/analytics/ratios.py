"""
Profitability Ratio Engine

"""

import math


def net_profit_margin(net_profit, sales):
    """
    Net Profit Margin = (Net Profit / Sales) * 100
    """

    if sales is None or sales == 0:
        return None

    return round((net_profit / sales) * 100, 2)


def operating_profit_margin(operating_profit, sales):
    """
    Operating Profit Margin = (Operating Profit / Sales) * 100
    """

    if sales is None or sales == 0:
        return None

    return round((operating_profit / sales) * 100, 2)


def validate_opm(calculated_opm, source_opm):
    """
    Returns True if calculated OPM differs by more than 1%
    """

    if calculated_opm is None or source_opm is None:
        return False

    return abs(calculated_opm - source_opm) > 1


def return_on_equity(net_profit, equity_capital, reserves):
    """
    ROE = Net Profit / (Equity + Reserves)
    """

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round((net_profit / equity) * 100, 2)


def return_on_capital_employed(
    operating_profit,
    interest,
    equity_capital,
    reserves,
    borrowings
):
    """
    ROCE = EBIT / Capital Employed
    EBIT = Operating Profit + Interest
    """

    capital = equity_capital + reserves + borrowings

    if capital <= 0:
        return None

    ebit = operating_profit + interest

    return round((ebit / capital) * 100, 2)


def return_on_assets(net_profit, total_assets):
    """
    ROA = Net Profit / Total Assets
    """

    if total_assets is None or total_assets == 0:
        return None

    return round((net_profit / total_assets) * 100, 2)

def debt_to_equity(borrowings, equity_capital, reserves):
    equity = equity_capital + reserves

    if borrowings == 0:
        return 0

    if equity <= 0:
        return None

    return round(borrowings / equity, 2)


def high_leverage_flag(de_ratio, sector):
    if de_ratio is None:
        return False

    return de_ratio > 5 and sector != "Financials"


def interest_coverage_ratio(
        operating_profit,
        other_income,
        interest):

    if interest == 0:
        return None

    return round(
        (operating_profit + other_income) / interest,
        2
    )


def icr_label(interest):
    if interest == 0:
        return "Debt Free"

    return None


def icr_warning(icr):
    if icr is None:
        return False

    return icr < 1.5


def net_debt(borrowings, investments):
    return borrowings - investments


def asset_turnover_ratio(sales, total_assets):
    if total_assets == 0:
        return None

    return round(sales / total_assets, 2)