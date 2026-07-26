import pandas as pd

from src.etl.validator import (
    check_duplicates,
    check_nulls,
    validate_positive,
)


def test_check_nulls():
    df = pd.DataFrame({"A": [1, None, 3], "B": [4, 5, None]})

    result = check_nulls(df)

    assert result["A"] == 1
    assert result["B"] == 1


def test_check_duplicates():
    df = pd.DataFrame({"A": [1, 1], "B": [2, 2]})

    assert check_duplicates(df) == 1


def test_validate_positive_true():
    s = pd.Series([1, 2, 3])

    assert validate_positive(s) == True


def test_validate_positive_false():
    s = pd.Series([1, -2, 3])

    assert validate_positive(s) == False
