# RealTimeSentimentAnalysisTwitter

This Spark Streaming application analyzes the sentiment of Twitter data in real-time using Apache Spark, NLTK's VADER Sentiment Analyzer, and the Tweepy library for accessing the Twitter API.

## Prerequisites
- Python
- Apache Spark
- NLTK
- Tweepy
- Twitter API credentials (consumer key, consumer secret, access token, and access token secret)

## Install the required Python libraries:
  pip install nltk tweepy

## Download NLTK's VADER lexicon:
   python -m nltk.downloader vader_lexicon

Replace the Twitter API credentials in the code with your own:
- consumer_key
- consumer_secret
- access_token
- access_token_secret

## Usage
1. Start the Spark Streaming application:
   spark-submit real_time_sentiment_analysis.py
2. Ingest Twitter data by running a socket server (e.g., Netcat) and sending tweets as text to the specified port (default: 5555).
3. The application will calculate the sentiment scores for the incoming tweets and display the results in real-time on the console.

