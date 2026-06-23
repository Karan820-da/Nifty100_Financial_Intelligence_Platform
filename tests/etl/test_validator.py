import pandas as pd
from src.etl.validator import check_duplicates


def test_duplicates():
    df = pd.DataFrame({"a": [1, 1]})
    assert check_duplicates(df) == 1