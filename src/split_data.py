import pandas as pd

from sklearn.model_selection import train_test_split

customers = pd.read_csv("data/customers.csv")

X=customers[
    [
        "age",
        "membership_years",
        "total_orders",
        "average_order_value",
        "total_spending",
        "days_since_last_purchase",

    ]
]
y=customers["churn"]

X_train, X_test, y_train, y_test=train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)
print("Training features:",X_train.shape)
print("Testing features:",X_test.shape)
print("Training targets:", y_train.shape)
print("Testiing targets:", y_test.shape)