import glob
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"
OUTPUT_FILE = DATA_DIR / "pink_morsel_sales.csv"


def load_and_transform(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df = df[df["product"].str.lower() == "pink morsel"].copy()
    df["price"] = df["price"].str.replace("$", "", regex=False).astype(float)
    df["Sales"] = df["quantity"] * df["price"]
    df["Date"] = df["date"]
    df["Region"] = df["region"]
    return df[["Sales", "Date", "Region"]]


def main() -> None:
    csv_files = sorted(DATA_DIR.glob("daily_sales_data_*.csv"))
    combined = pd.concat([load_and_transform(path) for path in csv_files], ignore_index=True)
    combined.to_csv(OUTPUT_FILE, index=False)
    print(f"Wrote {len(combined)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
