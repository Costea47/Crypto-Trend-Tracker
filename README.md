# Crypto-Trend-Tracker

## Overview

**Crypto-Trend-Tracker** is a Python-based tool designed to help cryptocurrency enthusiasts and investors analyze market trends, sentiment, and news to make better-informed decisions. This project collects and integrates data from multiple sources — including market prices, Google search trends, news articles, Reddit, and Twitter — to provide a comprehensive overview of popular cryptocurrencies' current status and sentiment.

The tool also leverages OpenAI's GPT-4 to synthesize all the gathered data and provide an AI-generated summary and insight about potential market movements.

---

## Features

- Fetches real-time cryptocurrency market data (price, market cap, 24h change).
- Collects Google Trends data to assess search interest in selected coins.
- Scrapes recent news articles related to cryptocurrencies and analyzes sentiment.
- Pulls Reddit posts and comments to gauge community sentiment.
- Gathers tweets for sentiment analysis on social media buzz.
- Uses OpenAI GPT-4 to generate a summary analysis based on the aggregated data.
- Saves combined data and insights into an Excel file for easy review.

---

## APIs and Libraries Used

| API/Library                                                                | Purpose                                                        |
| -------------------------------------------------------------------------- | -------------------------------------------------------------- |
| [CoinGecko API](https://www.coingecko.com/en/api)                          | Fetches cryptocurrency price, market cap, and volume data.     |
| [Google Trends API (PyTrends)](https://github.com/GeneralMills/pytrends)   | Collects search interest data for cryptocurrencies.            |
| [NewsAPI](https://newsapi.org/)                                            | Gathers recent news articles for sentiment analysis.           |
| [PRAW (Python Reddit API Wrapper)](https://praw.readthedocs.io/en/stable/) | Accesses Reddit posts and comments for community sentiment.    |
| [Tweepy](https://docs.tweepy.org/en/stable/)                               | Fetches recent tweets related to cryptocurrencies.             |
| [TextBlob](https://textblob.readthedocs.io/en/dev/)                        | Performs sentiment analysis on news, Reddit, and Twitter data. |
| [OpenAI GPT-4](https://platform.openai.com/docs/models/gpt-4)              | Generates natural language summaries and insights.             |
| [Pandas](https://pandas.pydata.org/)                                       | Handles data manipulation and exports results to Excel.        |

---

## How It Works

1. **Data Collection:**  
   The script fetches market data for selected cryptocurrencies via CoinGecko API.  
   It retrieves Google Trends data to understand public interest dynamics.  
   It scrapes recent news articles, Reddit posts, and tweets for sentiment analysis.

2. **Sentiment Analysis:**  
   TextBlob analyzes the sentiment polarity of news headlines, Reddit comments, and tweets to quantify market mood.

3. **AI Insight Generation:**  
   The aggregated data and sentiment scores are passed as a prompt to OpenAI GPT-4, which generates a summary of the current market outlook and potential price movements.

4. **Output:**  
   Results are printed to the console and saved in an Excel file (`Crypto_Trend_Tracker_Auto.xlsx`) combining raw data and AI-generated insights for further review.

---

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/Crypto-Trend-Tracker.git
   cd Crypto-Trend-Tracker
   ```

## Installation and Setup

Install dependencies:

`pip install -r requirements.txt`

Set up API keys in the script or environment variables:

- OpenAI API key

- NewsAPI key

- Reddit API credentials (client_id, client_secret, user_agent)

- Twitter API credentials (API key, API secret, Access token, Access secret)

Run the tracker:

`python crypto_trend_tracker.py`

## Output Example

The script outputs the following information for each cryptocurrency analyzed:

- Current price, market cap, and 24-hour price change.

- Google Trends interest score over the last 7 days.

- Average sentiment scores from News, Reddit, and Twitter.

- An AI-generated textual summary highlighting market sentiment and potential trends.

## The detailed data and insights are saved in Crypto_Trend_Tracker_Auto.xlsx.
