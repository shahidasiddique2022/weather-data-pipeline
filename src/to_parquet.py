
import pandas as pd
import os
from datetime import datetime


def csv_to_parquet():

    silver_folder = "data/silver"
    gold_folder = "data/gold"

    # Ensure folders exist
    os.makedirs(gold_folder, exist_ok=True)

    # Find all CSV files in Silver
    if not os.path.exists(silver_folder):
        print("Silver folder does not exist.")
        return

    csv_files = [
        f for f in os.listdir(silver_folder)
        if f.endswith(".csv")
    ]

    if not csv_files:
        print("No CSV files found in Silver layer.")
        return

    for file in csv_files:

        # Define source CSV path
        csv_path = os.path.join(silver_folder, file)

        # Create output Parquet filename
        base_name = file.replace(".csv", "")
        parquet_name = base_name + ".parquet"
        parquet_path = os.path.join(gold_folder, parquet_name)

        # Read CSV into a DataFrame
        df = pd.read_csv(csv_path)

        # Convert DataFrame to Parquet
        df.to_parquet(parquet_path, index=False)

        print(f"[OK] Converted to Parquet: {parquet_path}")


def main():
    print("Converting Silver CSVs to Parquet...")
    csv_to_parquet()
    print("Conversion process finished.")


if __name__ == "__main__":
    main()
