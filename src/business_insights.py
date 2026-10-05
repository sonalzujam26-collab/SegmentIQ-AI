import pandas as pd


# --------------------------------------------------
# 1. Load original customer features
# --------------------------------------------------

customer_file = "data/processed/customer_features.csv"
segment_file = "data/processed/customer_segments.csv"

customers = pd.read_csv(customer_file)
segments = pd.read_csv(segment_file)

# Keep only the customer ID and assigned cluster
segments = segments[["Customer ID", "Cluster"]]

# Merge cluster information with original features
df = customers.merge(
    segments,
    on="Customer ID",
    how="inner"
)


# --------------------------------------------------
# 2. Create cluster profile using original values
# --------------------------------------------------

features = [
    "Recency",
    "Frequency",
    "Monetary",
    "TotalQuantity",
    "UniqueProducts",
    "AverageOrderValue"
]

profile = df.groupby("Cluster")[features].mean()


# --------------------------------------------------
# 3. Add customer count
# --------------------------------------------------

customer_counts = (
    df["Cluster"]
    .value_counts()
    .sort_index()
)

profile["CustomerCount"] = customer_counts


# --------------------------------------------------
# 4. Add customer percentage
# --------------------------------------------------

profile["CustomerPercentage"] = (
    profile["CustomerCount"]
    / len(df)
    * 100
)


# --------------------------------------------------
# 5. Display profile
# --------------------------------------------------

print("\n" + "=" * 70)
print("CUSTOMER SEGMENT BUSINESS PROFILE")
print("=" * 70)

print(
    profile.round(2).to_string()
)


# --------------------------------------------------
# 6. Identify segment characteristics
# --------------------------------------------------

print("\n" + "=" * 70)
print("SEGMENT INTERPRETATION")
print("=" * 70)


for cluster in profile.index:

    row = profile.loc[cluster]

    print(f"\nCluster {cluster}")
    print("-" * 40)

    print(
        f"Customers: {int(row['CustomerCount'])}"
    )

    print(
        f"Customer Share: "
        f"{row['CustomerPercentage']:.2f}%"
    )

    print(
        f"Average Recency: "
        f"{row['Recency']:.2f} days"
    )

    print(
        f"Average Frequency: "
        f"{row['Frequency']:.2f} orders"
    )

    print(
        f"Average Monetary Value: "
        f"{row['Monetary']:.2f}"
    )

    print(
        f"Average Total Quantity: "
        f"{row['TotalQuantity']:.2f}"
    )

    print(
        f"Average Unique Products: "
        f"{row['UniqueProducts']:.2f}"
    )

    print(
        f"Average Order Value: "
        f"{row['AverageOrderValue']:.2f}"
    )


# --------------------------------------------------
# 7. Save business profile
# --------------------------------------------------

output_path = "data/processed/business_segment_profiles.csv"

profile.to_csv(output_path)

print("\nBusiness segment profile saved to:")
print(output_path)

print("\nBusiness insights analysis completed successfully!")