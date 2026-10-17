import pandas as pd
import os
from datetime import datetime
def csv_to_parquet():
silver_folder = "data/silver"
gold_folder = "data/gold"
# Ensure folders exist
os.makedirs(gold_folder, exist_ok=True)
# Find all CSVs in Silver
csv_files = [
f for f in os.listdir(silver_folder)
if f.endswith(".csv")
]
if not csv_files:
print("No CSV files found in Silver layer.")
return
for file in csv_files:
csv_path = os.path.join(silver_folder, file)
# Example filename: clean_2025-01-24.csv
base_name = file.replace(".csv", "")
parquet_name = base_name + ".parquet"
parquet_path = os.path.join(gold_folder, parquet_name)
df = pd.read_csv(csv_path)
df.to_parquet(parquet_path, index=False)
print(f"[OK] Converted to Parquet {parquet_path}")
def main():
print("Converting Silver CSVs to Parquet...")
csv_to_parquet()
if __name__ == "__main__":
main()
