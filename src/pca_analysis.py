import pandas as pd

from sklearn.decomposition import PCA


# --------------------------------------------------
# 1. Load scaled customer data
# --------------------------------------------------

input_path = "data/processed/customer_segments.csv"

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
# 2. Apply PCA
# --------------------------------------------------

pca = PCA(
    n_components=2,
    random_state=42
)

pca_result = pca.fit_transform(X)


# --------------------------------------------------
# 3. Add PCA components
# --------------------------------------------------

df["PC1"] = pca_result[:, 0]
df["PC2"] = pca_result[:, 1]


# --------------------------------------------------
# 4. Explained variance
# --------------------------------------------------

pc1_variance = pca.explained_variance_ratio_[0]
pc2_variance = pca.explained_variance_ratio_[1]

total_variance = (
    pc1_variance +
    pc2_variance
)


print("\nPCA completed successfully.")

print("\nExplained Variance:")

print(
    f"PC1: {pc1_variance:.2%}"
)

print(
    f"PC2: {pc2_variance:.2%}"
)

print(
    f"PC1 + PC2: {total_variance:.2%}"
)


# --------------------------------------------------
# 5. Save PCA dataset
# --------------------------------------------------

output_path = "data/processed/customer_segments_pca.csv"

df.to_csv(
    output_path,
    index=False
)

print("\nPCA dataset saved to:")
print(output_path)