import requests
import pandas as pd

# Define the API key and URL
api_key = "64PQ5AUnrPph0uYqVtINCzIHXk1ySabJ"
url = f"https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2023-01-09/2023-02-10?adjusted=true&sort=asc&apiKey={api_key}"

# Make the API request
try:
    print("Making API request to:", url)
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    data = response.json()
    print("API request successful. Data received.")
except requests.exceptions.RequestException as e:
    print(f"Error during API request: {e}")
    exit(1)

# Extract the results
results = data.get("results", [])
if not results:
    print("No results found in the response.")
    exit(1)

# Convert results to a DataFrame
try:
    df = pd.DataFrame(results)
    print("Data converted to DataFrame.")
except Exception as e:
    print(f"Error converting data to DataFrame: {e}")
    exit(1)

# Export DataFrame to CSV
try:
    df.to_csv("aggregates.csv", index=False)
    print("Data saved to aggregates.csv")
except Exception as e:
    print(f"Error saving data to CSV: {e}")
    exit(1)