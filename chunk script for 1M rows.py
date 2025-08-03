import pandas as pd

# Define the chunk size
chunk_size = 500000  # Adjust this based on your needs

# Read the large CSV file in chunks
csv_file = 'aggregated_data_072824_raw.csv'
chunk_iter = pd.read_csv(csv_file, chunksize=chunk_size)

# Initialize a counter for file naming
file_number = 1

# Loop through the chunks and save each one as a new CSV file
for chunk in chunk_iter:
    chunk.to_csv(f'aggdata_chunk_{file_number}.csv', index=False)
    file_number += 1

print(f"Successfully split the large CSV into {file_number - 1} smaller files.")
