import pandas as pd
import joblib

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

customers=pd.read_csv("data/customers.csv")

X=customers[
    [
        "total_orders",
        "average_order_value",
        "days_since_last_purchase",
        "total_spending",
    ]
]

scaler=StandardScaler()
X_scaled=scaler.fit_transform(X)

model =KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10,
)

customers["segment"]=model.fit_predict(X_scaled)

summary=customers.groupby("segment").agg(
    customers_count=("customer_id","count"),
    average_orders=("total_orders","mean"),
    average_order_value=("average_order_value","mean"),
    average_days_since_purchase=(
        "days_since_last_purchase","mean"
    ),
    average_spending=("total_spending","mean"),
)

print("\nCUSTOMER SEGMENT SUMMARY")
print(summary.round(2))

joblib.dump(scaler,"models/kmeans_scaler.pkl")
joblib.dump(model,"models/kmeans.pkl")

customers.to_csv(
    "reports/customer_segment.csv",
    index=False,
)

print("\nK-Means model and customer segment saved!")