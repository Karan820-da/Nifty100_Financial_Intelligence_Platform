import unittest

from src.screener.engine import load_config


class TestEngine(unittest.TestCase):

    def test_load_config(self):

        config = load_config()

        self.assertIn(
            "quality_compounder",
            config
        )

        self.assertIn(
            "value_pick",
            config
        )


if __name__ == "__main__":
    unittest.main()