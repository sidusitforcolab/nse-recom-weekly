
import pandas as pd
import yfinance as yf
from prophet import Prophet
from datetime import datetime, timedelta
import os
import warnings

warnings.filterwarnings("ignore")

# 📁 Output directory
os.makedirs("output", exist_ok=True)

# ✅ Load ticker symbols from CSV
try:
    df_symbols = pd.read_csv("nse_stock_list.csv")
    symbols = df_symbols["SYMBOL"].dropna().unique().tolist()
    tickers = [symbol.strip().upper() + ".NS" for symbol in symbols]
    print(f"✅ Loaded {len(tickers)} tickers from CSV.")
except Exception as e:
    print("❌ Error reading CSV:", e)
    tickers = []

# 📅 Set date range
end = datetime.today()
start = end - timedelta(days=365 * 1.5)

results = []

for ticker in tickers:
    print(f"📈 Processing {ticker} ...")
    try:
        df = yf.download(ticker, start=start, end=end)[['Adj Close']]
    except:
        continue

    if df.empty or len(df) < 250:
        print(f"⚠️ Not enough data for {ticker}. Skipping.")
        continue

    df.reset_index(inplace=True)
    df.rename(columns={'Date': 'ds', 'Adj Close': 'y'}, inplace=True)

    try:
        model = Prophet(daily_seasonality=False, weekly_seasonality=True, yearly_seasonality=True)
        model.fit(df)

        future = model.make_future_dataframe(periods=7)
        forecast = model.predict(future)

        last_price = df['y'].iloc[-1]
        predicted_price = forecast['yhat'].iloc[-1]
        return_pct = (predicted_price - last_price) / last_price * 100

        results.append({
            "Symbol": ticker.replace(".NS", ""),
            "Forecast Return %": round(return_pct, 2)
        })
    except Exception as e:
        print(f"❌ Error with {ticker}: {e}")
        continue

# ✅ Rank and output
df_results = pd.DataFrame(results).sort_values(by="Forecast Return %", ascending=False)
top5 = df_results.head(5)
top5.to_csv("output/weekly_top_stocks.csv", index=False)

print("\n✅ Top 5 Recommendations:")
print(top5)
