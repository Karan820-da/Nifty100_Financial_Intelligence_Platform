import unittest

from src.analytics.cashflow_kpis import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate,
    capital_allocation_pattern
)


class TestCashflow(unittest.TestCase):

    def test_free_cash_flow(self):
        self.assertEqual(
            free_cash_flow(
                100,
                -40
            ),
            60
        )

    def test_cfo_quality_high(self):
        self.assertEqual(
            cfo_quality_score(
                200,
                100
            ),
            "High Quality"
        )

    def test_cfo_quality_moderate(self):
        self.assertEqual(
            cfo_quality_score(
                75,
                100
            ),
            "Moderate"
        )

    def test_cfo_quality_risk(self):
        self.assertEqual(
            cfo_quality_score(
                20,
                100
            ),
            "Accrual Risk"
        )

    def test_capex_intensity(self):
        self.assertEqual(
            capex_intensity(
                -20,
                1000
            ),
            "Asset Light"
        )

    def test_fcf_conversion(self):
        self.assertEqual(
            fcf_conversion_rate(
                100,
                200
            ),
            50.0
        )

    def test_reinvestor_pattern(self):
        self.assertEqual(
            capital_allocation_pattern(
                100,
                -100,
                -50
            ),
            "Reinvestor"
        )

    def test_shareholder_returns(self):
        self.assertEqual(
            capital_allocation_pattern(
                100,
                -100,
                -50,
                "High Quality"
            ),
            "Shareholder Returns"
        )
        

if __name__ == "__main__":
    unittest.main()