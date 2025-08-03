import os
import requests
import pandas as pd
from datetime import datetime

# Define the API key and base URLs
api_key = "64PQ5AUnrPph0uYqVtINCzIHXk1ySabJ"
base_url_agg = "https://api.polygon.io/v2/aggs/ticker/{}/range/1/day"
base_url_sma = "https://api.polygon.io/v1/indicators/sma/{}"

# Define the date range
start_date = "2019-01-01"
end_date = "2024-08-20"

# List of tickers to fetch data for
tickers = ["GOOGL", "AAPL", "AMZN", "META", "NVDA", "TSLA"]

# Fetch aggregate bars data
def fetch_aggregate_data(ticker, start_date, end_date):
    print(f"Fetching aggregate data for {ticker} from {start_date} to {end_date}...")
    url = f"{base_url_agg.format(ticker)}/{start_date}/{end_date}?adjusted=true&sort=asc&apiKey={api_key}"
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
            print(f"Aggregate data for {ticker} fetched successfully.")
            return df
        else:
            print(f"No aggregate data found for {ticker} in the specified date range.")
            return pd.DataFrame()  # Return an empty DataFrame
    except requests.exceptions.RequestException as e:
        print(f"Error during API request for {ticker} aggregate data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame

# Fetch SMA data with pagination handling
def fetch_sma_data(ticker, sma_period):
    print(f"Fetching {sma_period}-day SMA data for {ticker}...")
    start_timestamp = int(pd.to_datetime(start_date).timestamp() * 1000)
    end_timestamp = int(pd.to_datetime(end_date).timestamp() * 1000)
    
    url = (f"{base_url_sma.format(ticker)}?timespan=day&adjusted=true&window={sma_period}&series_type=close"
           f"&timestamp.gte={start_timestamp}&timestamp.lte={end_timestamp}&apiKey={api_key}")
    
    all_data = []
    
    while url:
        try:
            response = requests.get(url, timeout=120)
            response.raise_for_status()
            data = response.json()
            results = data.get('results', {}).get('values', [])
            all_data.extend(results)

            # Check if there is a next page of data
            next_url = data.get('next_url', None)
            if next_url:
                url = f"{next_url}&apiKey={api_key}"
            else:
                url = None
                
        except requests.exceptions.RequestException as e:
            print(f"Error during API request for {sma_period}-day SMA for {ticker}: {e}")
            return pd.DataFrame()  # Return an empty DataFrame
    
    if all_data:
        df = pd.DataFrame(all_data)
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.date
        df.rename(columns={'value': f'SMA_{sma_period}d'}, inplace=True)
        print(f"{sma_period}-day SMA data for {ticker} fetched successfully.")
        return df[['date', f'SMA_{sma_period}d']]
    else:
        print(f"No data found for {sma_period}-day SMA for {ticker}.")
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

# Calculate 1-day percentage change
def calculate_1day_change(df):
    print("Calculating 1-day percentage change...")
    df['1DayChange'] = (df['Close'] - df['Close'].shift(1)) / df['Close'].shift(1) * 100
    print("1-day percentage change calculation complete.")
    return df

# Main function to combine everything for each ticker
def create_combined_csv_for_ticker(ticker):
    print(f"Starting data collection and combination process for {ticker}...")

    # Fetch aggregate data
    agg_df = fetch_aggregate_data(ticker, start_date, end_date)
    
    if agg_df.empty:
        print(f"No aggregate data to process for {ticker}.")
        return
    
    # Calculate overnight gap
    agg_df = calculate_overnight_gap(agg_df)
    
    # Calculate 1-day percentage change
    agg_df = calculate_1day_change(agg_df)
    
    # Fetch and merge SMA data in increasing order
    sma_periods = [10, 20, 50, 200]
    for period in sma_periods:
        sma_df = fetch_sma_data(ticker, period)
        if not sma_df.empty:
            agg_df = pd.merge(agg_df, sma_df, on='date', how='left')

    # Calculate and add ATR columns
    atr_periods = [1, 3, 5, 7, 14, 28]
    for period in atr_periods:
        agg_df = calculate_atr(agg_df, period)

    # Save the combined DataFrame to a CSV file
    filename = f"{ticker}_daily_aggregate_SMA_ATR_{start_date}_{end_date}.csv"
    agg_df.to_csv(filename, mode='w', header=True, index=False)
    print(f"Combined aggregate, SMA, ATR, and 1-day change data for {ticker} saved successfully as {filename}.")

# Run the main function for each ticker
for ticker in tickers:
    create_combined_csv_for_ticker(ticker)
