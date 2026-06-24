import pandas as pd
from sqlalchemy import create_engine

print("Nifty100 Financial Intelligence Platform")
print("ETL Pipeline Started...")

# =====================================
# MySQL Connection
# =====================================

username = "root"
password = "**********"
host = "localhost"
port = "3306"
database = "nifty100_db"

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)

print("Connected to MySQL successfully!")

# =====================================
# Companies File
# =====================================

file_path = r"data\raw\supporting_dataset\financial_ratios.xlsx"    #---------

# Check available sheets
excel_file = pd.ExcelFile(file_path)

print("\nAvailable Sheets:")
print(excel_file.sheet_names)

# Read Companies sheet
df = pd.read_excel(
    file_path,
    sheet_name="Sheet1",      #---------
    header=0
)

print("\nDataset Loaded Successfully!")
print("-" * 60)

print("\nFirst 5 Rows:")
print(df.head())

print("\nColumns:")
print(df.columns.tolist())

print("\nRows:", len(df))

# =====================================
# Load into MySQL
# =====================================

try:
    df.to_sql(
      name="financial_ratios",  #---------
        con=engine,
        if_exists="append",
        index=False
    )

    print(f"\n✅ {len(df)} rows inserted into MySQL table 'financial_ratios' successfully!")

except Exception as e:
    print("\n❌ ERROR:")
    print(e)

print("\nETL Pipeline Completed!")