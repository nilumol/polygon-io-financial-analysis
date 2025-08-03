import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

# Define the API key and base URLs
api_key = "64PQ5AUnrPph0uYqVtINCzIHXk1ySabJ"
ticker = "NVDA"
base_url_agg = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day"
base_url_sma = f"https://api.polygon.io/v1/indicators/sma/{ticker}"

# Define the date range
start_date = "2019-01-01"
# Set the date to the previous day
end_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')


# Fetch aggregate bars data
def fetch_aggregate_data(start_date, end_date):
    print(f"Fetching aggregate data from {start_date} to {end_date}...")
    url = f"{base_url_agg}/{start_date}/{end_date}?adjusted=true&sort=asc&apiKey={api_key}"
    try:
        response = requests.get(url)
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

# Fetch SMA data (no pagination handling, as API limit removed)
def fetch_sma_data(sma_period):
    print(f"Fetching {sma_period}-day SMA data...")
    start_timestamp = int(pd.to_datetime(start_date).timestamp() * 1000)
    end_timestamp = int(pd.to_datetime(end_date).timestamp() * 1000)
    
    url = (f"{base_url_sma}?timespan=day&adjusted=true&window={sma_period}&series_type=close"
           f"&timestamp.gte={start_timestamp}&timestamp.lte={end_timestamp}&apiKey={api_key}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        results = data.get('results', {}).get('values', [])
        
        if results:
            df = pd.DataFrame(results)
            df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.date
            df.rename(columns={'value': f'SMA_{sma_period}d'}, inplace=True)
            print(f"{sma_period}-day SMA data fetched successfully.")
            return df[['date', f'SMA_{sma_period}d']]
        else:
            print(f"No data found for {sma_period}-day SMA.")
            return pd.DataFrame()  # Return an empty DataFrame
    
    except requests.exceptions.RequestException as e:
        print(f"Error during API request for {sma_period}-day SMA: {e}")
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
    print(f"{period}-day ATR calculati
          on complete.")
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
    df['1 Day Change %'] = (df['Close'] - df['Close'].shift(1)) / df['Close'].shift(1) * 100
    print("1-day percentage change calculation complete.")
    return df

# Save DataFrame to Excel
def save_to_excel(agg_df):
    file_name = f'{ticker}_daily_aggregate_beta_{start_date}_{end_date}_prod.xlsx'
    file_path = os.path.join('/Users/wnilumol/VSC Projects/IBKR/beta scripts/', file_name)
    
    try:
        if os.path.exists(file_path):
            # Open the existing Excel file
            with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                # Write new data to the existing sheet (assuming 'Sheet1')
                agg_df.to_excel(writer, sheet_name='Sheet1', index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
            print(f"Excel file '{file_name}' updated with new data.")
        else:
            # Create a new Excel file if it doesn't exist
            agg_df.to_excel(file_path, index=False, engine='xlsxwriter')
            print(f"New Excel file '{file_name}' created and saved.")

    except Exception as e:
        print(f"Error opening or saving the file: {e}")


# Combine everything and save
def create_combined_csv():
    print("Starting data collection and combination process...")

    # Fetch aggregate data
    agg_df = fetch_aggregate_data(start_date, end_date)
    
    if agg_df.empty:
        print("No aggregate data to process.")
        return

    # Calculate overnight gap
    agg_df = calculate_overnight_gap(agg_df)
    
    # Calculate 1-day percentage change
    agg_df = calculate_1day_change(agg_df)
    
    # Fetch and merge SMA data in increasing order
    sma_periods = [10, 20, 50, 200]
    for period in sma_periods:
        sma_df = fetch_sma_data(period)
        if not sma_df.empty:
            agg_df = pd.merge(agg_df, sma_df, on='date', how='left')

    # Calculate ATR columns
    atr_periods = [1, 3, 5, 7, 14, 28]
    for period in atr_periods:
        agg_df = calculate_atr(agg_df, period)

    # Save to Excel
    save_to_excel(agg_df)

# Run the main function
create_combined_csv()
