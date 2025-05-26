import requests
import pandas as pd
from pytrends.request import TrendReq
from openai import OpenAI
import praw
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

# ========== CONFIG ==========
OPENAI_API_KEY = "your_openai_api_key"
NEWSAPI_KEY = "your_newsapi_key"
CRYPTOPANIC_API_KEY = "your_cryptopanic_api_key"
REDDIT_CLIENT_ID = "your_reddit_client_id"
REDDIT_CLIENT_SECRET = "your_reddit_client_secret"
REDDIT_USER_AGENT = "your_reddit_user_agent"
TWITTER_BEARER_TOKEN = "your_twitter_bearer_token"

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize PyTrends
pytrends = TrendReq(hl='en-US', tz=360)

# Initialize Sentiment Analyzer
sentiment_analyzer = SentimentIntensityAnalyzer()

# Initialize Reddit client
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# Initialize Twitter client (using Tweepy with bearer token for v2 endpoints)
twitter_client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

# ========== FUNCTIONS ==========

def fetch_news_newsapi(query, page_size=10):
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&pageSize={page_size}&apiKey={NEWSAPI_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        return [{"title": a["title"], "url": a["url"], "description": a["description"]} for a in articles]
    else:
        print(f"NewsAPI Error: {response.status_code}")
        return []

def fetch_news_cryptopanic():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTOPANIC_API_KEY}&public=true"
    response = requests.get(url)
    if response.status_code == 200:
        posts = response.json().get('results', [])
        return [{"title": p["title"], "url": p["url"], "source": p.get("source", {}).get("title", "")} for p in posts]
    else:
        print(f"CryptoPanic Error: {response.status_code}")
        return []

def fetch_reddit_posts(subreddit, query, limit=10):
    posts = []
    for submission in reddit.subreddit(subreddit).search(query, limit=limit, sort='new'):
        posts.append({
            "title": submission.title,
            "score": submission.score,
            "url": submission.url,
            "selftext": submission.selftext
        })
    return posts

def fetch_twitter_tweets(query, max_results=10):
    tweets = []
    try:
        response = twitter_client.search_recent_tweets(query=query, max_results=max_results, tweet_fields=['text', 'created_at'])
        if response.data:
            for tweet in response.data:
                tweets.append({"text": tweet.text, "created_at": tweet.created_at.isoformat()})
    except Exception as e:
        print(f"Twitter API Error: {e}")
    return tweets

def analyze_sentiment(text):
    score = sentiment_analyzer.polarity_scores(text)
    return score  # dict with pos, neu, neg, compound

def get_trend_score(coin):
    try:
        pytrends.build_payload([coin], timeframe='now 7-d')
        trends = pytrends.interest_over_time()
        if not trends.empty:
            return trends[coin].iloc[-1]
    except Exception as e:
        print(f"Google Trends error for {coin}: {e}")
    return 0

def get_coingecko_data(coin):
    try:
        url = f'https://api.coingecko.com/api/v3/coins/{coin}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            market = data.get('market_data', {})
            return {
                "Coin": data.get("name", coin),
                "Current Price (USD)": market.get("current_price", {}).get("usd"),
                "Market Cap (USD)": market.get("market_cap", {}).get("usd"),
                "24h Volume (USD)": market.get("total_volume", {}).get("usd"),
                "24h % Change": market.get("price_change_percentage_24h")
            }
    except Exception as e:
        print(f"CoinGecko error for {coin}: {e}")
    return None

# Helper function to clean text for prompt
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# ========== MAIN ==========

if __name__ == "__main__":
    # Example usage for coin 'bitcoin'
    coin = "bitcoin"

    print(f"Fetching news about {coin}...")
    news = fetch_news_newsapi(coin)
    news_cp = fetch_news_cryptopanic()
    reddit_posts = fetch_reddit_posts("cryptocurrency", coin)
    tweets = fetch_twitter_tweets(coin)

    print(f"Analyzing sentiment for {coin} data...")
    news_sentiments = [analyze_sentiment(clean_text(n['title'] + ' ' + (n.get('description') or ''))) for n in news]
    reddit_sentiments = [analyze_sentiment(clean_text(p['title'] + ' ' + p.get('selftext', ''))) for p in reddit_posts]
    tweets_sentiments = [analyze_sentiment(clean_text(t['text'])) for t in tweets]

    avg_news_sentiment = sum(s['compound'] for s in news_sentiments)/len(news_sentiments) if news_sentiments else 0
    avg_reddit_sentiment = sum(s['compound'] for s in reddit_sentiments)/len(reddit_sentiments) if reddit_sentiments else 0
    avg_tweet_sentiment = sum(s['compound'] for s in tweets_sentiments)/len(tweets_sentiments) if tweets_sentiments else 0

    trend_score = get_trend_score(coin)
    cg_data = get_coingecko_data(coin)

    summary = f"""
    Coin: {coin}
    Current Price: {cg_data['Current Price (USD)']}
    Market Cap: {cg_data['Market Cap (USD)']}
    24h Change: {cg_data['24h % Change']}
    Google Trends Score (last 7 days): {trend_score:.2f}
    Average News Sentiment: {avg_news_sentiment:.2f}
    Average Reddit Sentiment: {avg_reddit_sentiment:.2f}
    Average Twitter Sentiment: {avg_tweet_sentiment:.2f}
    """

    print(summary)

    # Build prompt for ChatGPT
    prompt = f"""
    Based on the following data for {coin}, provide your assessment of the likelihood this coin will grow by at least 10% in the next week:

    {summary}

    Please explain your reasoning.
    """

    print("Asking ChatGPT...")
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300
    )

    print("ChatGPT response:")
    print(response.choices[0].message.content)
