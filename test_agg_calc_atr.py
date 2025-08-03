import os
import requests
import pandas as pd
from datetime import datetime

# Define the API key and base URLs
api_key = "64PQ5AUnrPph0uYqVtINCzIHXk1ySabJ"
ticker = "AAPL"
base_url_agg = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day"

# Define the date range
start_date = "2023-01-09"
end_date = "2024-08-20"

# Fetch aggregate bars data
def fetch_aggregate_data(start_date, end_date):
    print(f"Fetching aggregate data from {start_date} to {end_date}...")
    url = f"{base_url_agg}/{start_date}/{end_date}?adjusted=true&sort=asc&apiKey={api_key}"
    try:
        response = requests.get(url, timeout=120)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        if results:
            df = pd.DataFrame(results)
            df['Ticker'] = ticker
            df['date'] = pd.to_datetime(df['t'], unit='ms').dt.date
            df.rename(columns={'o': 'Open', 'c': 'Close', 'h': 'High', 'l': 'Low', 'v': 'Volume'}, inplace=True)
            df = df[['Ticker', 'date', 'Open', 'Close', 'High', 'Low', 'Volume']]
            print("Aggregate data fetched successfully.")
            return df
        else:
            print(f"No aggregate data found for the specified date range.")
            return pd.DataFrame()  # Return an empty DataFrame
    except requests.exceptions.RequestException as e:
        print(f"Error during API request for aggregate data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame

# Calculate ATR for a given period
def calculate_atr(df, period):
    print(f"Calculating {period}-day ATR...")
    df['High-Low'] = df['High'] - df['Low']
    df['High-PrevClose'] = abs(df['High'] - df['Close'].shift(1))
    df['Low-PrevClose'] = abs(df['Low'] - df['Close'].shift(1))
    df['True Range'] = df[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis=1)
    atr_column_name = f'ATR_{period}d'
    df[atr_column_name] = df['True Range'].rolling(window=period).mean()
    df.drop(columns=['High-Low', 'High-PrevClose', 'Low-PrevClose', 'True Range'], inplace=True)
    print(f"{period}-day ATR calculation complete.")
    return df

# Calculate overnight gap and percentage
def calculate_overnight_gap(df):
    print("Calculating overnight gaps...")
    df['Overnight Gap'] = df['Open'] - df['Close'].shift(1)
    df['Overnight Gap %'] = (df['Overnight Gap'] / df['Close'].shift(1)) * 100
    print("Overnight gap calculation complete.")
    return df

# Main function to combine everything
def create_combined_csv():
    print("Starting data collection and combination process...")

    # Fetch aggregate data
    agg_df = fetch_aggregate_data(start_date, end_date)
    
    if agg_df.empty:
        print("No aggregate data to process.")
        return
    
    # Calculate overnight gap
    agg_df = calculate_overnight_gap(agg_df)
    
    # Calculate and add ATR columns
    atr_periods = [1, 3, 5, 7, 14, 28]
    for period in atr_periods:
        agg_df = calculate_atr(agg_df, period)

    # Save the combined DataFrame to a CSV file
    filename = f"{ticker}_daily_aggregate_ATR_{start_date}_{end_date}.csv"
    agg_df.to_csv(filename, mode='w', header=True, index=False)
    print(f"Combined aggregate, gap, and ATR data saved successfully as {filename}.")

# Run the main function
create_combined_csv()
