from src.reports.data_loader import (
    load_company,
    load_profit_loss,
    load_ratios,
    load_balance_sheet,
)

company_id = "TCS"

print("\nCompany")
print(load_company(company_id).head())

print("\nProfit & Loss")
print(load_profit_loss(company_id).head())

print("\nFinancial Ratios")
print(load_ratios(company_id).head())

print("\nBalance Sheet")
print(load_balance_sheet(company_id).head())