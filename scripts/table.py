import pandas as pd
from scripts.data_fetcher import fetch_options_data

# Fetch data
df, spot = fetch_options_data("SPY")

print(f"\n--- SPOT PRICE: ${spot:.2f} ---")
print("\n--- TABLE DATA SUMMARY ---")

# Group by expiration and count contracts and calculate days to expiry
summary = df.groupby('expiration').agg(
    Calls_Raw=('strike', 'count'),
    Days_To_Expiry=('daysToExpiration', 'first')
).reset_index()

# Sort by expiration date
summary = summary.sort_values('daysToExpiration')

print(summary.to_string(index=False))