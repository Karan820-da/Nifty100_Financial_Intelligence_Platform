import pandas as pd
from unittest.mock import patch

from src.etl.loader import load_excel


sample_df = pd.DataFrame({
    "A": [1, 2],
    "B": [3, 4]
})


@patch("src.etl.loader.pd.read_excel")
def test_load_returns_dataframe(mock_read):
    mock_read.return_value = sample_df

    df = load_excel("dummy.xlsx", "Sheet1")

    assert isinstance(df, pd.DataFrame)


@patch("src.etl.loader.pd.read_excel")
def test_row_count(mock_read):
    mock_read.return_value = sample_df

    df = load_excel("dummy.xlsx", "Sheet1")

    assert len(df) == 2


@patch("src.etl.loader.pd.read_excel")
def test_column_count(mock_read):
    mock_read.return_value = sample_df

    df = load_excel("dummy.xlsx", "Sheet1")

    assert len(df.columns) == 2


@patch("src.etl.loader.pd.read_excel")
def test_column_names(mock_read):
    mock_read.return_value = sample_df

    df = load_excel("dummy.xlsx", "Sheet1")

    assert list(df.columns) == ["A", "B"]


@patch("src.etl.loader.pd.read_excel")
def test_sheet_name_argument(mock_read):
    mock_read.return_value = sample_df

    load_excel("dummy.xlsx", "Companies")

    mock_read.assert_called_once()


@patch("src.etl.loader.pd.read_excel")
def test_header_default(mock_read):
    mock_read.return_value = sample_df

    load_excel("dummy.xlsx", "Sheet1")

    assert mock_read.call_args.kwargs["header"] == 0


@patch("src.etl.loader.pd.read_excel")
def test_custom_header(mock_read):
    mock_read.return_value = sample_df

    load_excel("dummy.xlsx", "Sheet1", header=2)

    assert mock_read.call_args.kwargs["header"] == 2


@patch("src.etl.loader.pd.read_excel")
def test_file_path(mock_read):
    mock_read.return_value = sample_df

    load_excel("financials.xlsx", "Sheet1")

    assert mock_read.call_args.args[0] == "financials.xlsx"

@patch("src.etl.loader.pd.read_excel")
def test_sheet_parameter(mock_read):
    mock_read.return_value = sample_df

    load_excel("dummy.xlsx", "Ratios")

    assert mock_read.call_args.kwargs["sheet_name"] == "Ratios"


@patch("src.etl.loader.pd.read_excel")
def test_same_dataframe_returned(mock_read):
    mock_read.return_value = sample_df

    df = load_excel("dummy.xlsx", "Sheet1")

    assert df.equals(sample_df)