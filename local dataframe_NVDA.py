import pandas as pd

# Load your CSV file
file_path = '/Users/wnilumol/VSC Projects/IBKR/files 083024/NVDA_daily_aggregate_SMA_ATR_2019-01-01_2024-08-20.csv'
df = pd.read_csv(file_path)

# Make sure 'date' column is in datetime format
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

# Merge weekly and monthly data
weekly_data['date'] = weekly_data.index
monthly_data['date'] = monthly_data.index

# Saving to CSV
combined_data = pd.concat([weekly_data, monthly_data], axis=1)

combined_data.to_csv('weekly_monthly_atr_gain_loss.csv', index=False)

print("Weekly and monthly ATR, along with gain/loss percentages, saved to CSV.")
