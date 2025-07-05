import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import os

# Define your stock universe (NSE tickers via Yahoo Finance)
stocks = ['RELIANCE.NS', 'INFY.NS', 'TCS.NS', 'HDFCBANK.NS', 'ICICIBANK.NS',
          'KOTAKBANK.NS', 'SBIN.NS', 'LT.NS', 'BHARTIARTL.NS', 'AXISBANK.NS']

# Define the past week's date range
end_date = datetime.today()
start_date = end_date - timedelta(days=7)

# Collect price data
data = yf.download(stocks, start=start_date, end=end_date)['Adj Close']

# Drop columns with all NaNs
data = data.dropna(axis=1, how='all')

# Calculate returns
returns = (data.iloc[-1] - data.iloc[0]) / data.iloc[0] * 100

# Create a DataFrame of results
result_df = pd.DataFrame({
    "Symbol": returns.index.str.replace('.NS', '', regex=False),
    "Weekly Return %": returns.values
}).sort_values(by="Weekly Return %", ascending=False)

# Select top 5
top_picks = result_df.head(5)

# Save output
os.makedirs("output", exist_ok=True)
top_picks.to_csv("output/weekly_top_stocks.csv", index=False)

print("✅ Weekly stock recommendation complete. Output saved.")