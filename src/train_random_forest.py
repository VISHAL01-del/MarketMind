import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import(
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)

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

X_train,X_test,y_train,y_test=train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

model =RandomForestClassifier(
    n_estimators=200,
    max_depth=200,
    random_state=42,
    n_jobs=-1,
)

model.fit(X_train,y_train)

churn_probabilties=model.predict_proba(X_test)[:,1]

y_pred = (churn_probabilties >= 0.3).astype(int)

print("Accuracy:", round(accuracy_score(y_test, y_pred), 3))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("ROC-AUC:", round(roc_auc_score(y_test, churn_probabilties), 3))

# 10. Save the trained model
joblib.dump(model, "models/random_forest.pkl")

print("\nRandom Forest saved successfully!")