import pandas as pd

import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import(
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

customers=pd.read_csv("data/customers.csv")

X=customers[
    [
        "age",
        "membership_years",
        "total_orders",
        "average_order_value",
        "days_since_last_purchase",
    ]
]

y=customers["total_spending"]
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

model =LinearRegression()

model.fit(X_train,y_train)

predictions=model.predict(X_test)

mae=mean_absolute_error(y_test,predictions)
mse=mean_squared_error(y_test,predictions)

r2=r2_score(y_test,predictions)

print("Mean Absolute Error:", round(mae, 2))
print("Mean Squared Error:", round(mse, 2))
print("R2 Score:", round(r2, 3))

# 9. Save the model
joblib.dump(model, "models/linear_regression.pkl")
print("\nLinear Regression saved successfully!")
