import pandas as pd

# Load your CSV file
file_path = '/Users/wnilumol/VSC Projects/IBKR/files 083024/NVDA_daily_aggregate_SMA_ATR_2019-01-01_2024-08-20.csv'
df = pd.read_csv(file_path)

# Ensure 'date' column is in datetime format
df['date'] = pd.to_datetime(df['date'])

# Set the index to 'date'
df.set_index('date', inplace=True)

# Function to calculate ATR
def calculate_atr(data):
    data['high_low'] = data['High'] - data['Low']
    data['high_close'] = (data['High'] - data['Close'].shift()).abs()
    data['low_close'] = (data['Low'] - data['Close'].shift()).abs()
    true_range = data[['high_low', 'high_close', 'low_close']].max(axis=1)
    atr = true_range.mean()  # Calculating the mean ATR for the period
    return atr

# Weekly resample
weekly_data = df.resample('W').agg({
    'Open': 'first',
    'Close': 'last',
    'High': 'max',
    'Low': 'min',
    'Volume': 'sum'
})

# Calculate Weekly ATR
weekly_data['weekly_atr'] = df.resample('W').apply(calculate_atr)

# Weekly gain/loss in terms of price difference
weekly_data['week_gain_loss'] = weekly_data['Close'] - weekly_data['Open']

# Weekly gain/loss in percentage
weekly_data['week_gain_loss_%'] = (weekly_data['week_gain_loss'] / weekly_data['Open']) * 100

# Monthly resample
monthly_data = df.resample('M').agg({
    'Open': 'first',
    'Close': 'last',
    'High': 'max',
    'Low': 'min',
    'Volume': 'sum'
})

# Calculate Monthly ATR
monthly_data['monthly_atr'] = df.resample('M').apply(calculate_atr)

# Monthly gain/loss in terms of price difference
monthly_data['month_gain_loss'] = monthly_data['Close'] - monthly_data['Open']

# Monthly gain/loss in percentage
monthly_data['month_gain_loss_%'] = (monthly_data['month_gain_loss'] / monthly_data['Open']) * 100

# Combine the weekly and monthly data
combined_data = pd.concat([weekly_data, monthly_data], axis=0)

# Sort by date to maintain the order of both weekly and monthly data
combined_data.sort_index(inplace=True)

# Reset index to have the 'date' column properly aligned
combined_data.reset_index(inplace=True)

# Save to CSV
output_file_path = '/Users/wnilumol/VSC Projects/IBKR/files 083024/combined_weekly_monthly_atr.csv'
combined_data.to_csv(output_file_path, index=False)

print("Combined weekly and monthly ATR, gain/loss percentages, saved to CSV.")
