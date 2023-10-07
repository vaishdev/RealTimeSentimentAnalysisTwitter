# -*- coding: utf-8 -*-
"""Real time Sentiment analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sNKf__3AS4Ff5EBDJaJogSnS79yJbiIg
"""

import tweepy
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, expr
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

# Initialize NLTK's VADER Sentiment Analyzer
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# Twitter API credentials (replace with your own)
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Initialize a SparkSession
spark = SparkSession.builder.appName("RealTimeSentimentAnalysis").getOrCreate()

# Define the schema for the incoming Twitter data
schema = StructType([
    StructField("text", StringType(), True),
])

# Create a streaming query to read the data from Twitter
query = spark.readStream.format("socket") \
    .option("host", "localhost") \
    .option("port", 5555) \
    .load() \
    .selectExpr("CAST(value AS STRING) AS text")

# Define a Python function to calculate sentiment
def calculate_sentiment(text):
    sentiment = sia.polarity_scores(text)
    return sentiment['compound']  # Using the compound score as overall sentiment

# Register the Python function as a UDF
calculate_sentiment_udf = udf(calculate_sentiment, DoubleType())

# Process the data to calculate the sentiment of the tweets
processed_data = query.withColumn("sentiment", calculate_sentiment_udf(query["text"]))

# Create a streaming query to display the sentiment of the tweets
query = processed_data.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# Wait for the query to finish
query.awaitTermination()