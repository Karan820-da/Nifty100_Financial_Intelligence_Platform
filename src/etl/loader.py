import pandas as pd


def load_excel(file_path, sheet_name, header=0):
    df = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        header=header
    )
    return df