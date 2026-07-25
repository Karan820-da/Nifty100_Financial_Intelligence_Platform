import pytest

from src.analytics.ratios import *


def test_net_profit_margin():
    assert net_profit_margin(20, 100) == 20.0


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(20, 0) is None


def test_operating_profit_margin():
    assert operating_profit_margin(25, 100) == 25.0


def test_validate_opm_match():
    assert validate_opm(20, 20.5) is False


def test_validate_opm_mismatch():
    assert validate_opm(20, 25) is True


def test_return_on_equity():
    assert return_on_equity(20, 50, 50) == 20.0


def test_negative_equity():
    assert return_on_equity(20, -10, 5) is None


def test_return_on_assets():
    assert return_on_assets(25, 100) == 25.0


def test_debt_to_equity():
    assert debt_to_equity(50, 50, 50) == 0.5


def test_debt_free_de_ratio():
    assert debt_to_equity(0, 100, 100) == 0


def test_high_leverage_flag():
    assert high_leverage_flag(6, "Industrials") is True


def test_high_leverage_financials():
    assert high_leverage_flag(6, "Financials") is False


def test_interest_coverage_ratio():
    assert interest_coverage_ratio(100, 20, 10) == 12.0


def test_interest_coverage_none():
    assert interest_coverage_ratio(100, 20, 0) is None


def test_icr_label():
    assert icr_label(0) == "Debt Free"


def test_icr_warning():
    assert icr_warning(1.2) is True


def test_net_debt():
    assert net_debt(100, 30) == 70


def test_asset_turnover():
    assert asset_turnover_ratio(200, 100) == 2.0


def test_asset_turnover_zero_assets():
    assert asset_turnover_ratio(100, 0) is None


def test_roce():
    assert return_on_capital_employed(
        100,
        20,
        100,
        100,
        100
    ) == 40.0