
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
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

# 2. Select input features
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

# 4. Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

# 5. Create the ML pipeline
model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(max_iter=1000)),
])

# 6. Train the model
model.fit(X_train, y_train)

# 7. Save the trained model
joblib.dump(model, "models/logistic_regression.pkl")
print("Model saved successfully!")

# 8. Get churn probabilities
churn_probabilities = model.predict_proba(X_test)[:, 1]

# 9. Convert probabilities into predictions
y_pred = (churn_probabilities >= 0.3).astype(int)

# 10. Evaluate the model
cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:")
print(cm)

print("\nAccuracy:", round(accuracy_score(y_test, y_pred), 3))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

roc_auc = roc_auc_score(y_test, churn_probabilities)
print("ROC-AUC Score:", round(roc_auc, 3))
