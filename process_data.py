import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
dfs = []

for csv_file in DATA_DIR.glob("*.csv"):
    df = pd.read_csv(csv_file)

    # Normalize product
    df["product"] = df["product"].str.strip().str.lower()
    df = df[df["product"] == "pink morsel"]

    # 🔥 FIX: clean price and quantity
    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .astype(float)
    )

    df["quantity"] = df["quantity"].astype(int)

    # Correct sales calculation
    df["Sales"] = df["quantity"] * df["price"]

    df = df[["Sales", "date", "region"]].rename(
        columns={"date": "Date", "region": "Region"}
    )

    dfs.append(df)

final_df = pd.concat(dfs, ignore_index=True)

# Aggregate per day & region (important!)
final_df = (
    final_df
    .groupby(["Date", "Region"], as_index=False)["Sales"]
    .sum()
)

final_df.to_csv("pink_morsel_sales.csv", index=False)

print("✅ pink_morsel_sales.csv recreated correctly")
