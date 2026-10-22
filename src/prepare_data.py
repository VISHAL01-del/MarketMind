import pandas as pd

customers=pd.read_csv("data/customers.csv")
X=customers[
    [
        "age",
        "membership_years",
        "total_orders",
        "average_order_value",
        "days_since_last_purchase",
        "total_spending",
    ]
]
y=customers["churn"]
print("Features shape:",X.shape)
print("Target shape:",y.shape)

print("\nFirst five feature rows:")
print(X.head())

print("\nFirst five target values:")
print(y.head())