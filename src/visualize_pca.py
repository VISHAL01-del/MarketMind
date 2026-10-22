import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

customers=pd.read_csv("reports/customer_segment.csv")
print("Dataset shape:",customers.shape)
print("\nFirst five customers:")
print(customers.head())

features=[
    "total_orders",
    "average_order_value",
    "days_since_last_purchase",
    "total_spending",
]

X=customers[features]

scaler=StandardScaler()
X_scaled=scaler.fit_transform(X)
print("\nScaled dats shape:",X_scaled.shape)

pca =PCA(n_components=2)

X_pca =pca.fit_transform(X_scaled)

print("\n.PCA dat shape:",X_pca.shape)

print(
    "Variance explained :",
    pca.explained_variance_ratio_.round(3)
)

print(
    "Total variance explained :",
    round(pca.explained_variance_ratio_.sum()*100,2),
    "%"
)

## scatter plot

plt.figure(figsize=(10,7))

scatter = plt.scatter(
    X_pca[:, 0],
    X_pca[:, 1],
    c=customers["segment"],
    cmap="viridis",
    alpha=0.7,
    s=35,
)

plt.title("Customer Segments visualize with PCA")
plt.xlabel("Princpal Components 1")
plt.ylabel("Principal Components 2")

plt.colorbar(scatter, label="Customer segment")
plt.grid(alpha=0.2)
plt.tight_layout()
plt.savefig("images/customer_segments_pca.png", dpi=300)
plt.show()

print("\nPCA visualization saved to images/customer_segments_pca.png")