import os

import routers.sentiment as sentiment
import tweepy
from dotenv import load_dotenv
from fastapi import APIRouter

tweets_router = APIRouter()
load_dotenv()
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_key = os.getenv('ACCESS_KEY')
access_secret = os.getenv('ACCESS_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key,
                      access_secret)

api = tweepy.API(auth)


@tweets_router.get("/{stock}/tweets")
async def get_stock_tweets(stock: str):
    results = api.search(q=stock, count=5, tweet_mode='extended')
    tweets = []
    for tweet in results:
        tweets.append(tweet.full_text)
    confidence = sentiment.average_sentiment(tweets)
    return [{"tweets": tweets, "confidence": confidence}]