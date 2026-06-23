import pandas as pd


def check_nulls(df):
    return df.isnull().sum()


def check_duplicates(df):
    return df.duplicated().sum()


def validate_positive(column):
    return (column >= 0).all()