import unittest

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    validate_opm,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets
)


class TestProfitabilityRatios(unittest.TestCase):

    def test_net_profit_margin(self):
        self.assertEqual(net_profit_margin(100, 1000), 10.00)

    def test_net_profit_margin_zero_sales(self):
        self.assertIsNone(net_profit_margin(100, 0))

    def test_operating_profit_margin(self):
        self.assertEqual(operating_profit_margin(150, 1000), 15.00)

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


if __name__ == "__main__":
    unittest.main()