import unittest

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    validate_opm,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    icr_label,
    icr_warning,
    net_debt,
    asset_turnover_ratio
)


class TestProfitabilityRatios(unittest.TestCase):

    # ===== Day 08 Tests =====

    def test_net_profit_margin(self):
        self.assertEqual(net_profit_margin(100, 1000), 10.00)

    def test_net_profit_margin_zero_sales(self):
        self.assertIsNone(net_profit_margin(100, 0))

    def test_operating_profit_margin(self):
        self.assertEqual(
            operating_profit_margin(150, 1000),
            15.00
        )

    def test_validate_opm_match(self):
        self.assertFalse(validate_opm(15.0, 15.5))

    def test_validate_opm_mismatch(self):
        self.assertTrue(validate_opm(15.0, 17.5))

    def test_return_on_equity(self):
        self.assertEqual(
            return_on_equity(100, 500, 500),
            10.00
        )

    def test_negative_equity(self):
        self.assertIsNone(
            return_on_equity(100, -500, -200)
        )

    def test_return_on_assets(self):
        self.assertEqual(
            return_on_assets(120, 1200),
            10.00
        )

    # ===== Day 09 Tests =====

    def test_debt_to_equity(self):
        self.assertEqual(
            debt_to_equity(100, 200, 300),
            0.20
        )

    def test_debt_free_de_ratio(self):
        self.assertEqual(
            debt_to_equity(0, 200, 300),
            0
        )

    def test_high_leverage_flag(self):
        self.assertTrue(
            high_leverage_flag(6.5, "Technology")
        )

    def test_high_leverage_financials(self):
        self.assertFalse(
            high_leverage_flag(6.5, "Financials")
        )

    def test_interest_coverage_ratio(self):
        self.assertEqual(
            interest_coverage_ratio(
                100,
                20,
                10
            ),
            12.0
        )

    def test_interest_coverage_none(self):
        self.assertIsNone(
            interest_coverage_ratio(
                100,
                20,
                0
            )
        )

    def test_icr_label(self):
        self.assertEqual(
            icr_label(0),
            "Debt Free"
        )

    def test_icr_warning(self):
        self.assertTrue(
            icr_warning(1.2)
        )

    def test_net_debt(self):
        self.assertEqual(
            net_debt(1000, 400),
            600
        )

    def test_asset_turnover(self):
        self.assertEqual(
            asset_turnover_ratio(
                1000,
                500
            ),
            2.0
        )


if __name__ == "__main__":
    unittest.main()