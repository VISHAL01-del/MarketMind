import numpy as np
import pandas as pd

# Make our random data reproducible
np.random.seed(42)

# Number of customers
n_customers = 1000

# Generate customer information
customer_id = np.arange(1, n_customers + 1)

age = np.random.randint(18, 70, n_customers)

membership_years = np.round(
    np.random.uniform(0.1, 10, n_customers), 1
)

total_orders = np.random.poisson(12, n_customers)

average_order_value = np.round(
    np.random.uniform(200, 5000, n_customers), 2
)

days_since_last_purchase = np.random.randint(
    1, 181, n_customers
)

# Combine everything into a table
customers = pd.DataFrame({
    "customer_id": customer_id,
    "age": age,
    "membership_years": membership_years,
    "total_orders": total_orders,
    "average_order_value": average_order_value,
    "days_since_last_purchase": days_since_last_purchase,
})

# Calculate total historical spending
customers["total_spending"] = (
    customers["total_orders"]
    * customers["average_order_value"]
)
# Create a synthetic churn target

# Higher inactivity increases churn risk
# More orders reduce churn risk
churn_score = (
    -3.0
    + 0.025 * customers["days_since_last_purchase"]
    - 0.06 * customers["total_orders"]
)

# Convert the score into a probability between 0 and 1
churn_probability = 1 / (1 + np.exp(-churn_score))

# Generate the simulated churn label
customers["churn"] = (
    np.random.rand(n_customers) < churn_probability
).astype(int)

# Display the churn distribution
print("\n--- CHURN DISTRIBUTION ---")
print(customers["churn"].value_counts())

# Display the first five customers
print(customers.head())

customers.to_csv("data/customers.csv",index=False)

print("Dataset saved successfully!")
print("Dataset shape:", customers.shape)