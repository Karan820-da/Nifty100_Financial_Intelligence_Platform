import pandas as pd
from sqlalchemy import create_engine

print("Nifty100 Financial Intelligence Platform")
print("ETL Pipeline Started...")

# mysql connection

username = "root"
password = "Kaikira820"
host = "localhost"
port = "3306"
database = "nifty100_db"

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)

print("Connected to MySQL successfully!")
# read excel file

file_path = r"data\raw\dataset\companies.xlsx"

df = pd.read_excel(
    file_path,
    sheet_name="Companies",
    header=1
)

print("\nCompanies Dataset Loaded Successfully!")
print(df.head())
print("\nColumn Names:")
print(df.columns.tolist())
print("\nLoading data into MySQL...")

df.to_sql(
    name="companies",
    con=engine,
    if_exists="append",
    index=False
)

print("Data loaded successfully!")
