import json
import os
from datetime import datetime
def get_latest_bronze_file(bronze_folder="data/bronze"):
    """
    Finds the most recent JSON file in the bronze folder.
    """
    if not os.path.exists(bronze_folder):
        raise FileNotFoundError(f"Bronze folder not found: {bronze_folder}")
    files = [
        f for f in os.listdir(bronze_folder)
        if f.endswith(".json")
    ]
    if not files:
        raise FileNotFoundError("No JSON files found in bronze layer.")
    # Sort files by name; if you used date-based names this works well
    files.sort()
    latest_file = files[-1]
    return os.path.join(bronze_folder, latest_file)
def load_bronze_json(filepath):
    """
    Loads JSON data from the given bronze file path.
    """
    with open(filepath, "r") as f:
        data = json.load(f)
    return data
def clean_weather(raw_json, city_name="Edmonton"):
    """
    Transforms raw Open-Meteo JSON into a list of rows:
    [
      {"timestamp": "...", "temp": 1.2, "city": "Edmonton"},
      ...
    ]
    """
    hourly = raw_json.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    if not times or not temps:
        raise ValueError("Missing 'time' or 'temperature_2m' in JSON.")
    if len(times) != len(temps):
        raise ValueError("Length mismatch between time and temperature lists.")
    rows = []
    for t, temp in zip(times, temps):
        rows.append(
            {
                "timestamp": t,
                "temp": temp,
                "city": city_name 
            }
        )
    return rows
def save_to_silver(rows, silver_folder="data/silver"):
    """
    Saves the cleaned rows to a CSV file in the silver layer.
    File name example: data/silver/clean_2025-01-22.csv
    """
    os.makedirs(silver_folder, exist_ok=True)
    today_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"clean_{today_str}.csv"
    filepath = os.path.join(silver_folder, filename)
    # We will use the built-in csv module to keep it very "Python basics"
    import csv
    fieldnames = ["timestamp", "temp", "city"]
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[OK] Cleaned data saved {filepath}")
def main():
    print("Loading latest bronze file...")
    bronze_path = get_latest_bronze_file()
    print(f"Using bronze file: {bronze_path}")
    raw_json = load_bronze_json(bronze_path)
    print("Cleaning weather data into tabular format...")
    rows = clean_weather(raw_json, city_name="Edmonton")
    print(f"Total rows: {len(rows)}")
    print("Saving to silver layer as CSV...")
    save_to_silver(rows)
    print("Silver layer updated successfully.")
if __name__ == "__main__":
  main()
