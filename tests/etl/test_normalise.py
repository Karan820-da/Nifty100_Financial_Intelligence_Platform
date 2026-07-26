
from src.etl.normalizer import normalize_year

# -------------------------
# Normal Cases
# -------------------------


def test_year_string():
    assert normalize_year("2024") == "2024"


def test_year_integer():
    assert normalize_year(2024) == "2024"


def test_year_float():
    assert normalize_year(2024.0) == "2024.0"


def test_strip_spaces():
    assert normalize_year(" 2024 ") == "2024"


def test_month_format():
    assert normalize_year("Mar 2024") == "Mar 2024"


def test_dec_format():
    assert normalize_year("Dec 2012") == "Dec 2012"


def test_numeric_string():
    assert normalize_year("1999") == "1999"


def test_single_digit():
    assert normalize_year(7) == "7"


# -------------------------
# Empty / Missing
# -------------------------


def test_empty_string():
    assert normalize_year("") == ""


def test_spaces_only():
    assert normalize_year("   ") == ""


def test_none():
    assert normalize_year(None) == "None"


# -------------------------
# Different Types
# -------------------------


def test_boolean_true():
    assert normalize_year(True) == "True"


def test_boolean_false():
    assert normalize_year(False) == "False"


def test_list():
    assert normalize_year([2024]) == "[2024]"


def test_tuple():
    assert normalize_year((2024,)) == "(2024,)"


def test_dictionary():
    assert normalize_year({"year": 2024}) == "{'year': 2024}"


# -------------------------
# Edge Cases
# -------------------------


def test_negative_year():
    assert normalize_year(-1) == "-1"


def test_zero():
    assert normalize_year(0) == "0"


def test_large_number():
    assert normalize_year(999999999) == "999999999"


def test_special_characters():
    assert normalize_year("@2024") == "@2024"
