from src.etl.normalizer import normalize_ticker


def test_normalize_ticker():
    assert normalize_ticker("tcs") == "TCS"