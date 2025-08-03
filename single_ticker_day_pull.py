import os
import requests
import pandas as pd
from datetime import datetime, timedelta
import time

# Define the API key and base URL
api_key = "64PQ5AUnrPph0uYqVtINCzIHXk1ySabJ"
ticker = "AAPL"
base_url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day"

# Create a directory to store the daily data
os.makedirs("daily_data", exist_ok=True)

# Function to fetch and save data for a given date range
def fetch_and_save_data(start_date, end_date):
    url = f"{base_url}/{start_date}/{end_date}?adjusted=true&sort=asc&apiKey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        if results:
            df = pd.DataFrame(results)
            df['Ticker'] = ticker  # Add ticker column
            df['date'] = pd.to_datetime(df['t'], unit='ms').dt.date  # Convert timestamp to date
            df.rename(columns={'o': 'Open', 'c': 'Close', 'h': 'High', 'l': 'Low', 'v': 'Volume'}, inplace=True)
            # Reorder columns to match desired format, with Ticker as the first column
            df = df[['Ticker', 'date', 'Open', 'Close', 'High', 'Low', 'Volume']]
            # Save to CSV
            filename = f"{ticker}_1_day_{start_date}_{end_date}.csv"
            df.to_csv(filename, mode='w', header=True, index=False)
            print(f"Data from {start_date} to {end_date} saved successfully as {filename}.")
        else:
            print(f"No data found for the specified date range.")
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")

# Calculate overnight price movement and percentage
def calculate_overnight_gap(csv_file):
    df = pd.read_csv(csv_file)
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by=['date'], inplace=True)
    df['Overnight Gap'] = df['Open'] - df['Close'].shift(1)
    df['Overnight Gap %'] = (df['Overnight Gap'] / df['Close'].shift(1)) * 100
    df.to_csv(csv_file, index=False)
    print(f"Overnight gap and percentage calculations added and saved to {csv_file}")

# Chunk the CSV file into smaller files
def chunk_csv_file(csv_file, chunk_size=500000):
    chunk_iter = pd.read_csv(csv_file, chunksize=chunk_size)
    file_number = 1
    base_filename = os.path.splitext(csv_file)[0]
    
    for chunk in chunk_iter:
        chunk_filename = f"{base_filename}_chunk_{file_number}.csv"
        chunk.to_csv(chunk_filename, index=False)
        print(f"Chunk {file_number} saved as {chunk_filename}")
        file_number += 1
    
    print(f"Successfully split the large CSV into {file_number - 1} smaller files.")

# Define the date range for fetching data
start_date = "2023-01-09"
end_date = "2024-08-20"

# Fetch data and save it to CSV
fetch_and_save_data(start_date, end_date)

# Perform overnight gap calculation
csv_filename = f"{ticker}_1_day_{start_date}_{end_date}.csv"
calculate_overnight_gap(csv_filename)

# Chunk the CSV file into smaller files
chunk_csv_file(csv_filename)
