import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

customers=pd.read_csv("data/customers.csv")

print("Dataset shape:",customers.shape)
print("\nAvailable columns:")
print(customers.columns.to_list())

features = [
    "age",
    "membership_years",
    "total_orders",
    "average_order_value",
    "days_since_last_purchase",
    "total_spending",
]

X = customers[features]

print("\nFeatures selected:", features)
print("Feature data shape:", X.shape)

scaler =StandardScaler()
X_scaled=scaler.fit_transform(X)

print("\nScaled data shape:",X_scaled.shape)
print("First customer,scaled features :")
print(X_scaled)

knn =NearestNeighbors(
    n_neighbors=6,
    metric="euclidean"
)
knn.fit(X_scaled)
print("\nKNN model iss ready")

# Select the first customer as our example
customer_index = 0

# Get this customer's features
query_customer = X_scaled[customer_index].reshape(1, -1)

# Find the nearest neighbors
distances, indices = knn.kneighbors(query_customer)

# Exclude the query customer itself
similar_indices = indices[0][1:]
similar_distances = distances[0][1:]

# Display the similar customers
similar_customers = customers.iloc[similar_indices].copy()
similar_customers["distance"] = similar_distances

print("\nQUERY CUSTOMER")
print(customers.iloc[customer_index])

print("\nFIVE MOST SIMILAR CUSTOMERS")
print(
    similar_customers[
        ["customer_id", "age", "total_orders",
         "average_order_value", "total_spending", "distance"]
    ].to_string(index=False)
)

## saving codde
joblib.dump(knn, "models/knn.pkl")
joblib.dump(scaler, "models/knn_scaler.pkl")

print("\nKNN model saved successfully!")