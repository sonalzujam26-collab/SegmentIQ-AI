import pandas as pd

file_path = "data/raw/online_retail_II.xlsx"

print("Loading dataset...")

excel_file = pd.ExcelFile(file_path)

print("\nSheets available:")
print(excel_file.sheet_names)

for sheet in excel_file.sheet_names:
    print("\n" + "=" * 60)
    print("SHEET:", sheet)
    print("=" * 60)

    df = pd.read_excel(file_path, sheet_name=sheet)

    print("\nRows and Columns:")
    print(df.shape)

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nFirst 5 Rows:")
    print(df.head())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nData Types:")
    print(df.dtypes)

print("\nDataset inspection completed successfully!")