import pandas as pd
from pathlib import Path

# Path to data folder
DATA_DIR = Path("data")

# List to hold processed dataframes
dfs = []

# Loop through all CSV files in data folder
for csv_file in DATA_DIR.glob("*.csv"):
    df = pd.read_csv(csv_file)

    # Keep only Pink Morsels
    df = df[df["product"] == "Pink Morsel"]

    # Create sales column
    df["Sales"] = df["quantity"] * df["price"]

    # Keep required columns
    df = df[["Sales", "date", "region"]]

    # Rename columns to match spec
    df = df.rename(columns={
        "date": "Date",
        "region": "Region"
    })

    dfs.append(df)

# Combine all regions into one dataframe
final_df = pd.concat(dfs, ignore_index=True)

# Write output file
final_df.to_csv("pink_morsel_sales.csv", index=False)

print("✅ pink_morsel_sales.csv created successfully")
