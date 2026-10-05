import pandas as pd


# --------------------------------------------------
# 1. Load both Excel sheets
# --------------------------------------------------

file_path = "data/raw/online_retail_II.xlsx"

print("Loading Excel dataset...")

df_2009 = pd.read_excel(
    file_path,
    sheet_name="Year 2009-2010"
)

df_2010 = pd.read_excel(
    file_path,
    sheet_name="Year 2010-2011"
)

print("Both sheets loaded successfully.")


# --------------------------------------------------
# 2. Combine both years
# --------------------------------------------------

df = pd.concat(
    [df_2009, df_2010],
    ignore_index=True
)

print("\nCombined dataset shape:")
print(df.shape)


# --------------------------------------------------
# 3. Remove rows without Customer ID
# --------------------------------------------------

df = df.dropna(subset=["Customer ID"])

print("\nAfter removing missing Customer IDs:")
print(df.shape)


# --------------------------------------------------
# 4. Remove cancelled invoices
# --------------------------------------------------

df = df[
    ~df["Invoice"].astype(str).str.startswith("C")
]

print("\nAfter removing cancelled invoices:")
print(df.shape)


# --------------------------------------------------
# 5. Keep valid quantities and prices
# --------------------------------------------------

df = df[
    (df["Quantity"] > 0) &
    (df["Price"] > 0)
]

print("\nAfter removing invalid Quantity and Price:")
print(df.shape)


# --------------------------------------------------
# 6. Create Revenue
# --------------------------------------------------

df["Revenue"] = df["Quantity"] * df["Price"]


# --------------------------------------------------
# 7. Create reference date
# --------------------------------------------------

reference_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)


# --------------------------------------------------
# 8. Create customer-level features
# --------------------------------------------------

customer_data = df.groupby("Customer ID").agg(
    Recency=(
        "InvoiceDate",
        lambda x: (reference_date - x.max()).days
    ),

    Frequency=(
        "Invoice",
        "nunique"
    ),

    Monetary=(
        "Revenue",
        "sum"
    ),

    TotalQuantity=(
        "Quantity",
        "sum"
    ),

    UniqueProducts=(
        "StockCode",
        "nunique"
    )
).reset_index()


# --------------------------------------------------
# 9. Create Average Order Value
# --------------------------------------------------

customer_data["AverageOrderValue"] = (
    customer_data["Monetary"] /
    customer_data["Frequency"]
)


# --------------------------------------------------
# 10. Save customer-level dataset
# --------------------------------------------------

output_path = "data/processed/customer_features.csv"

customer_data.to_csv(
    output_path,
    index=False
)


# --------------------------------------------------
# 11. Display final information
# --------------------------------------------------

print("\nCustomer-level dataset created successfully!")

print("\nCustomer feature shape:")
print(customer_data.shape)

print("\nCustomer feature columns:")
print(customer_data.columns.tolist())

print("\nFirst 5 customers:")
print(customer_data.head())

print("\nSaved to:")
print(output_path)