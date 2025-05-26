import requests
import pandas as pd
from pytrends.request import TrendReq

# Initialize Google Trends
pytrends = TrendReq(hl='en-US', tz=360)

# List of coins to track
coins = ['bitcoin', 'ethereum', 'solana']

# Create empty list for data
coin_data = []

# Fetch CoinGecko data
for coin in coins:
    url = f'https://api.coingecko.com/api/v3/coins/{coin}'
    response = requests.get(url).json()

    market_data = response.get("market_data", {})
    coin_name = response.get("name", coin)

    # Google Trends
    pytrends.build_payload([coin], cat=0, timeframe='now 7-d', geo='')
    trends = pytrends.interest_over_time()
    trend_score = trends[coin].iloc[-1] if not trends.empty else 0

    coin_data.append({
        "Coin": coin_name,
        "Current Price (USD)": market_data.get("current_price", {}).get("usd"),
        "Market Cap (USD)": market_data.get("market_cap", {}).get("usd"),
        "24h Volume (USD)": market_data.get("total_volume", {}).get("usd"),
        "24h % Change": market_data.get("price_change_percentage_24h"),
        "Google Trends Score": trend_score,
        "Notes": ""
    })

# Save to Excel
df = pd.DataFrame(coin_data)
df.to_excel("Crypto_Trend_Tracker_Live.xlsx", index=False)

print("Crypto trend tracker saved as 'Crypto_Trend_Tracker_Live.xlsx'")
