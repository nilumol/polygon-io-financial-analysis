import os
import requests
import pandas as pd
import time

# Define the API key and base URL
api_key = "64PQ5AUnrPph0uYqVtINCzIHXk1ySabJ"
ticker = "AAPL"
base_url = f"https://api.polygon.io/v1/indicators/sma/{ticker}"

# Define the date range globally so it can be accessed throughout the script
start_date = "2023-01-01"
end_date = "2023-01-21"  # Set end date if needed

# Define the SMA periods to fetch
sma_periods = [50, 10, 200, 20]

# Function to fetch SMA data
def fetch_sma_data(sma_period):
    # Convert date to timestamp in milliseconds
    start_timestamp = int(pd.to_datetime(start_date).timestamp() * 1000)
    end_timestamp = int(pd.to_datetime(end_date).timestamp() * 1000)
    
    # Construct the initial URL with timestamp filtering
    url = (f"{base_url}?timespan=day&adjusted=true&window={sma_period}&series_type=close"
           f"&timestamp.gte={start_timestamp}&timestamp.lte={end_timestamp}&apiKey={api_key}")
    
    all_data = []
    page_counter = 0
    
    while url:
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            results = data.get('results', {}).get('values', [])
            all_data.extend(results)

            # Log the current page and next URL
            page_counter += 1
            print(f"Page {page_counter} fetched with {len(results)} entries for {sma_period}-day SMA.")
            
            # Check if there is a next page of data
            next_url = data.get('next_url', None)
            if next_url:
                url = f"{next_url}&apiKey={api_key}"
                #time.sleep(15)  # Increase delay to avoid hitting the rate limit
            else:
                url = None
                
        except requests.exceptions.RequestException as e:
            print(f"Error during API request for {sma_period}-day SMA: {e}")
            return None
    
    if all_data:
        df = pd.DataFrame(all_data)
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.date
        df.rename(columns={'value': f'SMA_{sma_period}d', 'timestamp': 'Timestamp'}, inplace=True)
        df = df[['date', f'SMA_{sma_period}d']]
        return df
    else:
        print(f"No data found for {sma_period}-day SMA.")
        return None

# Fetch data for each SMA period and merge into a single DataFrame
all_sma_data = None
for period in sma_periods:
    sma_df = fetch_sma_data(period)
    if sma_df is not None:
        if all_sma_data is None:
            all_sma_data = sma_df
        else:
            all_sma_data = pd.merge(all_sma_data, sma_df, on='date', how='outer')

# Add ticker column and save to CSV if data was fetched
if all_sma_data is not None:
    all_sma_data['ticker'] = ticker
    valid_columns = ['ticker', 'date'] + [col for col in all_sma_data.columns if col.startswith('SMA_')]
    all_sma_data = all_sma_data[valid_columns]
    filename = f"{ticker}_all_SMAs_{start_date}_{end_date}.csv"
    all_sma_data.to_csv(filename, mode='w', header=True, index=False)
    print(f"All SMA data saved successfully as {filename}.")
else:
    print(f"No SMA data was fetched.")
