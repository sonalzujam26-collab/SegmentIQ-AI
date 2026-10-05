import pandas as pd
import pickle

from sklearn.cluster import KMeans


# --------------------------------------------------
# 1. Load scaled customer features
# --------------------------------------------------

input_path = "data/processed/customer_features_scaled.csv"

df = pd.read_csv(input_path)

features = [
    "Recency",
    "Frequency",
    "Monetary",
    "TotalQuantity",
    "UniqueProducts",
    "AverageOrderValue"
]

X = df[features]


# --------------------------------------------------
# 2. Create final K-Means model
# --------------------------------------------------

kmeans = KMeans(
    n_clusters=2,
    random_state=42,
    n_init=10
)

df["Cluster"] = kmeans.fit_predict(X)


# --------------------------------------------------
# 3. Save customer segments
# --------------------------------------------------

output_path = "data/processed/customer_segments.csv"

df.to_csv(
    output_path,
    index=False
)


# --------------------------------------------------
# 4. Save K-Means model
# --------------------------------------------------

model_path = "models/kmeans_model.pkl"

with open(model_path, "wb") as file:
    pickle.dump(kmeans, file)


# --------------------------------------------------
# 5. Display cluster sizes
# --------------------------------------------------

print("\nCluster sizes:")

print(
    df["Cluster"]
    .value_counts()
    .sort_index()
)


# --------------------------------------------------
# 6. Display cluster profiles
# --------------------------------------------------

profile = df.groupby("Cluster")[features].mean()

print("\nCluster Profiles:")

print(
    profile.round(2)
)


# --------------------------------------------------
# 7. Save cluster profiles
# --------------------------------------------------

profile.to_csv(
    "data/processed/cluster_profiles.csv"
)


print("\nCustomer segmentation completed successfully!")

print("\nCustomer segments saved to:")
print(output_path)

print("\nK-Means model saved to:")
print(model_path)

print("\nCluster profiles saved to:")
print("data/processed/cluster_profiles.csv")