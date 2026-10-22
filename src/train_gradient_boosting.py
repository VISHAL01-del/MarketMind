
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)

# Step 1: Load the data
customers = pd.read_csv("data/customers.csv")

# Step 2: Select input features
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

# Step 3: Select the target
y = customers["churn"]

# Step 4: Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

# Step 5: Create the model
model = GradientBoostingClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=3,
    random_state=42,
)

# Step 6: Train the model
model.fit(X_train, y_train)

# Step 7: Get churn probabilities
churn_probabilities = model.predict_proba(X_test)[:, 1]

# Step 8: Convert probabilities to predictions
y_pred = (churn_probabilities >= 0.3).astype(int)

# Step 9: Evaluate the model
print("Accuracy:", round(accuracy_score(y_test, y_pred), 3))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

print("ROC-AUC:", round(roc_auc_score(y_test, churn_probabilities), 3))

# Step 10: Save the model
joblib.dump(model, "models/gradient_boosting.pkl")
print("\nGradient Boosting saved successfully!")
