from utils.db import get_home_data

df = get_home_data()

print(df.head())

print(df.shape)