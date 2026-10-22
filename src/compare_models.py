
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)

# 1. Load the customer dataset
customers = pd.read_csv("data/customers.csv")

# 2. Select the same six features used for training
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

y = customers["churn"]

# 3. Recreate the same test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

# 4. List our six saved models
model_files = {
    "Logistic Regression": "models/logistic_regression.pkl",
    "Decision Tree": "models/decision_tree.pkl",
    "Random Forest": "models/random_forest.pkl",
    "Gradient Boosting": "models/gradient_boosting.pkl",
    "SVM": "models/svm.pkl",
    "XGBoost": "models/xgboost.pkl",
}

results = []

# 5. Load and evaluate each model
for model_name, file_path in model_files.items():
    model = joblib.load(file_path)

    # Get the probability of churn
    probabilities = model.predict_proba(X_test)[:, 1]

    # Apply the same threshold to every model
    predictions = (probabilities >= 0.3).astype(int)

    # Calculate evaluation metrics
    results.append({
        "Model": model_name,
        "Accuracy": round(
    float(accuracy_score(y_test, predictions)), 3
),
        "Precision": round(
            float(precision_score(y_test, predictions, zero_division=0)), 3
        ),
        "Recall": round(
            float(recall_score(y_test, predictions, zero_division=0)), 3
        ),
        "F1 Score": round(
            float(f1_score(y_test, predictions, zero_division=0)), 3
        ),
        "ROC-AUC": round(
            roc_auc_score(y_test, probabilities), 3
        ),
    })

# 6. Display the comparison
comparison = pd.DataFrame(results)
comparison = comparison.sort_values(
    by="ROC-AUC", ascending=False
)

print("\nMODEL COMPARISON")
print(comparison.to_string(index=False))

# 7. Save the report
comparison.to_csv(
    "reports/model_comparison.csv", index=False
)

print("\nComparison saved to reports/model_comparison.csv")
