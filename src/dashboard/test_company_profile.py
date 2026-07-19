from utils.db import get_company_profile

company_id = 1      # Replace with a valid company_id from your database

df = get_company_profile(company_id)

print(df.head())
print(df.shape)