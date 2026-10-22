
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)

# 1. Load the dataset
customers = pd.read_csv("data/customers.csv")

# 2. Select features
X = customers[
    [
        "age",
        "membership_years",
        "total_orders",
        "average_order_value",
        "days_since_last_purchase",
        "total_spending",
    ]
]

# 3. Select the target
y = customers["churn"]

# 4. Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

# 5. Create an SVM pipeline
model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", SVC(
        kernel="rbf",
        C=1.0,
        probability=True,
        random_state=42,
    )),
])

# 6. Train the model
model.fit(X_train, y_train)

# 7. Get churn probabilities
churn_probabilities = model.predict_proba(X_test)[:, 1]

# 8. Predict using threshold 0.3
y_pred = (churn_probabilities >= 0.3).astype(int)

# 9. Evaluate the model
print("Accuracy:", round(accuracy_score(y_test, y_pred), 3))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

print("ROC-AUC:", round(roc_auc_score(y_test, churn_probabilities), 3))

# 10. Save the model
joblib.dump(model, "models/svm.pkl")
print("\nSVM saved successfully!")
