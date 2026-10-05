import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# --------------------------------------------------
# 1. Load customer-level data
# --------------------------------------------------

file_path = "data/processed/customer_features.csv"

df = pd.read_csv(file_path)

print("Customer dataset loaded successfully.")

print("\nDataset shape:")
print(df.shape)


# --------------------------------------------------
# 2. Basic information
# --------------------------------------------------

print("\nColumn names:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())


# --------------------------------------------------
# 3. Statistical summary
# --------------------------------------------------

print("\nStatistical Summary:")
print(df.describe().round(2))


# --------------------------------------------------
# 4. Feature list
# --------------------------------------------------

features = [
    "Recency",
    "Frequency",
    "Monetary",
    "TotalQuantity",
    "UniqueProducts",
    "AverageOrderValue"
]


# --------------------------------------------------
# 5. Check skewness
# --------------------------------------------------

print("\nFeature Skewness:")

for feature in features:
    print(
        f"{feature}: "
        f"{df[feature].skew():.2f}"
    )


# --------------------------------------------------
# 6. Create distribution plots
# --------------------------------------------------

for feature in features:

    plt.figure(figsize=(8, 5))

    sns.histplot(
        df[feature],
        bins=40,
        kde=True
    )

    plt.title(f"Distribution of {feature}")
    plt.xlabel(feature)
    plt.ylabel("Number of Customers")

    plt.tight_layout()

    safe_name = (
        feature
        .lower()
        .replace(" ", "_")
    )

    plt.savefig(
        f"assets/{safe_name}_distribution.png",
        dpi=150
    )

    plt.close()


# --------------------------------------------------
# 7. Correlation heatmap
# --------------------------------------------------

plt.figure(figsize=(9, 7))

correlation = df[features].corr()

sns.heatmap(
    correlation,
    annot=True,
    fmt=".2f",
    cmap="Blues"
)

plt.title("Customer Feature Correlation")

plt.tight_layout()

plt.savefig(
    "assets/customer_feature_correlation.png",
    dpi=150
)

plt.close()


print("\nEDA completed successfully!")

print("\nEDA plots saved inside:")
print("assets/")