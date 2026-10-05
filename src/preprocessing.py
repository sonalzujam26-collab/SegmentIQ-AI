import pandas as pd
import numpy as np
import pickle

from sklearn.preprocessing import StandardScaler


# --------------------------------------------------
# 1. Load customer-level dataset
# --------------------------------------------------

input_path = "data/processed/customer_features.csv"

df = pd.read_csv(input_path)

print("Customer dataset loaded successfully.")

print("\nOriginal shape:")
print(df.shape)


# --------------------------------------------------
# 2. Select features for clustering
# --------------------------------------------------

features = [
    "Recency",
    "Frequency",
    "Monetary",
    "TotalQuantity",
    "UniqueProducts",
    "AverageOrderValue"
]

X = df[features].copy()


# --------------------------------------------------
# 3. Apply log transformation
# --------------------------------------------------

X_log = np.log1p(X)

print("\nLog transformation completed.")


# --------------------------------------------------
# 4. Apply StandardScaler
# --------------------------------------------------

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X_log)


# --------------------------------------------------
# 5. Convert scaled data back to DataFrame
# --------------------------------------------------

X_scaled_df = pd.DataFrame(
    X_scaled,
    columns=features
)

X_scaled_df.insert(
    0,
    "Customer ID",
    df["Customer ID"]
)


# --------------------------------------------------
# 6. Save scaled customer features
# --------------------------------------------------

output_path = "data/processed/customer_features_scaled.csv"

X_scaled_df.to_csv(
    output_path,
    index=False
)


# --------------------------------------------------
# 7. Save scaler
# --------------------------------------------------

scaler_path = "models/customer_scaler.pkl"

with open(scaler_path, "wb") as file:
    pickle.dump(scaler, file)


# --------------------------------------------------
# 8. Display results
# --------------------------------------------------

print("\nScaled dataset shape:")
print(X_scaled_df.shape)

print("\nScaled feature statistics:")

print(
    X_scaled_df[features]
    .describe()
    .loc[["mean", "std"]]
    .round(2)
)

print("\nFirst 5 scaled customers:")
print(X_scaled_df.head())

print("\nSaved scaled dataset to:")
print(output_path)

print("\nSaved scaler to:")
print(scaler_path)

print("\nPreprocessing completed successfully!")