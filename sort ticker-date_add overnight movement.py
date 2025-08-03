import pandas as pd

# Define the input and output file paths
input_csv_file = '/Users/wnilumol/VSC Projects/Data for BigQuery/files-scripts for data cleanup/aggdata_chunk_1_sheets.csv'
output_csv_file = '/Users/wnilumol/VSC Projects/Data for BigQuery/files-scripts for data cleanup/aggdata_chunk_1_sheets_sorted_2.csv'

# Read the CSV file
df = pd.read_csv(input_csv_file)

# Ensure data is sorted by Ticker and Date
df['Date'] = pd.to_datetime(df['Date'])
df.sort_values(by=['Ticker', 'Date'], inplace=True)

# Calculate Overnight Price Movement: Current day's open minus previous day's close
df['Overnight Price Movement'] = df['Open'] - df.groupby('Ticker')['Close'].shift(1)

# Save the sorted DataFrame with the new column to a new CSV file
df.to_csv(output_csv_file, index=False)

print(f"Data has been successfully sorted and saved to {output_csv_file}")
