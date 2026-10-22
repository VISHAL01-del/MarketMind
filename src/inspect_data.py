import pandas as pd
customers =pd.read_csv("data/customers.csv")

print("\n---First Five CUSTOMERS---")
print(customers.head())

print("\n---DATASET SHAPE---")
print(customers.shape)

print("\n---DATASET INFORMATION---")
customers.info()

print("\n---MISSING VALUES---")
print(customers.isnull().sum())