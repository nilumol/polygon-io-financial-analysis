import os
import requests
import pandas as pd
from datetime import datetime, timedelta
import time

# Define the API key and base URL
api_key = "64PQ5AUnrPph0uYqVtINCzIHXk1ySabJ"
base_url = "https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks"

# Create a directory to store the daily data
os.makedirs("daily_data", exist_ok=True)

# Function to fetch and save data for a given date
def fetch_and_save_data(date):
    url = f"{base_url}/{date}?adjusted=true&apiKey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        if results:
            df = pd.DataFrame(results)
            df['date'] = date  # Add the date column
            # Append to master CSV file
            df.to_csv("aggregated_data.csv", mode='a', header=not os.path.exists("aggregated_data.csv"), index=False)
            print(f"Data for {date} saved successfully.")
        else:
            print(f"No data found for {date}.")
    except requests.exceptions.RequestException as e:
        print(f"Error during API request for {date}: {e}")

# Function to generate dates for the given date range
def generate_dates(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days=1)

# Fetch data for the given date range
end_date = datetime.now().date()
start_date = datetime(2023, 1, 1).date()

for date in generate_dates(start_date, end_date):
    fetch_and_save_data(date.strftime("%Y-%m-%d"))
    time.sleep(12)  # Respect API rate limit (5 requests per minute)
