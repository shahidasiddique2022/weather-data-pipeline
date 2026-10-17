#Python packages we will be using 
import requests
import json
import logging
from datetime import datetime
import os
def fetch_weather():
url = (
"https://api.open-meteo.com/v1/forecast"
"?latitude=53.55&longitude=-113.46&hourly=temperature_2m"
)
try:
response = requests.get(url, timeout=10)  #requests.get-The most common Pyt
response.raise_for_status() #catch HTTP errors
data = response.json() #save data as json
 except Exception as e:
    logging.error(f"{datetime.now()} - API Error: {e}")
    return None
def save_to_bronze(data):
    # Make sure the folder exists
    os.makedirs("data/bronze", exist_ok=True)
    # File name example: data/bronze/2025-01-22.json
    filename = datetime.now().strftime("%Y-%m-%d.json")
    filepath = os.path.join("data/bronze", filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[OK] Raw weather saved {filepath}")
def main():
    print("Fetching weather data...")
    weather = fetch_weather()
    if weather:
        save_to_bronze(weather)
    else:
        print("❌
 No data received. Check logs for details.")
if __name__ == "__main__":
    main()
