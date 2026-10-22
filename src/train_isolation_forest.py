import pandas as pd
import joblib 
from sklearn.ensemble import IsolationForest

customers =pd.read_csv("data/customers.csv")

print("Dataset shape:",customers.shape)
print("\nFirst five customers:")
print(customers.head())

features = [
    "age",
    "membership_years",
    "total_orders",
    "average_order_value",
    "days_since_last_purchase",
    "total_spending",
]


X=customers[features]

print("\nSelected features:",features)
print("Features data shape:",X.shape)

model =IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42,
)

predictions=model.fit_predict(X)

normal_count = (predictions ==1).sum()
anomaly_count=(predictions ==-1).sum()

print("\nISOLATION FOREST RESULTS")
print("Normal reccords:",normal_count)
print("Potential anomalies:",anomaly_count)

customers["anomaly_prediction"]=predictions

customers["anomaly_status"]=customers["anomaly_prediction"].map({
    1:"Normal",
    -1:"Potential Anomaly",
})

customers["anomaly_status"]=customers["anomaly_prediction"].map({
    1:"Normal",
    -1:"potential Anomaly",
})

anomalies =customers[
    customers["anomaly_prediction"]==-1
]

print("\nFIRST 10 POTENTIAL ANOMALIES")
print(
    anomalies[
        [
            "customer_id",
            "total_orders",
            "average_order_value",
            "days_since_last_purchase",
            "total_spending",
            "anomaly_status",
        ]
    ].head(10).to_string(index=False)

)

customers.to_csv("reports/customer_anomalies.csv",index=False)

joblib.dump(model,"models/isolation_forest.pkl")
print("\nAnomaly report saved to reports/customer_anomalies.csv")
print("Isolation Forest model saved to models/isolation_forest.pkl")