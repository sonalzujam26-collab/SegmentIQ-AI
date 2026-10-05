import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# --------------------------------------------------
# 1. Load scaled customer features
# --------------------------------------------------

file_path = "data/processed/customer_features_scaled.csv"

df = pd.read_csv(file_path)

features = [
    "Recency",
    "Frequency",
    "Monetary",
    "TotalQuantity",
    "UniqueProducts",
    "AverageOrderValue"
]

X = df[features]

print("Scaled customer data loaded successfully.")
print("Dataset shape:", X.shape)


# --------------------------------------------------
# 2. Test different numbers of clusters
# --------------------------------------------------

k_values = range(2, 11)

inertia_values = []
silhouette_values = []


for k in k_values:

    print(f"\nTesting K = {k}")

    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = kmeans.fit_predict(X)

    inertia_values.append(
        kmeans.inertia_
    )

    score = silhouette_score(
        X,
        labels
    )

    silhouette_values.append(score)

    print(f"Inertia: {kmeans.inertia_:.2f}")
    print(f"Silhouette Score: {score:.4f}")


# --------------------------------------------------
# 3. Create Elbow Method plot
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    k_values,
    inertia_values,
    marker="o"
)

plt.title("Elbow Method")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia")
plt.xticks(list(k_values))

plt.tight_layout()

plt.savefig(
    "assets/elbow_method.png",
    dpi=150
)

plt.close()


# --------------------------------------------------
# 4. Create Silhouette Score plot
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    k_values,
    silhouette_values,
    marker="o"
)

plt.title("Silhouette Score by Number of Clusters")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Silhouette Score")
plt.xticks(list(k_values))

plt.tight_layout()

plt.savefig(
    "assets/silhouette_scores.png",
    dpi=150
)

plt.close()


# --------------------------------------------------
# 5. Display summary
# --------------------------------------------------

results = pd.DataFrame({
    "K": list(k_values),
    "Inertia": inertia_values,
    "Silhouette Score": silhouette_values
})

print("\n" + "=" * 60)
print("CLUSTERING ANALYSIS RESULTS")
print("=" * 60)

print(
    results.to_string(
        index=False,
        formatters={
            "Inertia": "{:.2f}".format,
            "Silhouette Score": "{:.4f}".format
        }
    )
)


best_k = results.loc[
    results["Silhouette Score"].idxmax(),
    "K"
]

best_score = results["Silhouette Score"].max()

print("\nHighest Silhouette Score:")
print(f"K = {int(best_k)}")
print(f"Score = {best_score:.4f}")

print("\nClustering analysis completed successfully!")