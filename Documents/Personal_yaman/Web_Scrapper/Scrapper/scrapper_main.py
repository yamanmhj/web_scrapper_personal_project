import asyncio
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint
from dataclasses import dataclass
import os
import twikit
from twikit import Client, TooManyRequests
import streamlit as st
import sys
from upload_S3 import upload_to_s3


@dataclass
class ScrapperTwitterDataconfig:
    WebScrapper_Store_path_root: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    Testing_dataset_path: str = os.path.join(WebScrapper_Store_path_root, 'DataSet', 'Scrapped_Data.csv')
    artifact_path: str = os.path.join(WebScrapper_Store_path_root, 'artifacts')
    config_path: str = os.path.join(WebScrapper_Store_path_root, 'config.ini')


class ScrapperTwitterData:
    def __init__(self, tweet_topic):
        self.ScrapperTwitterobj = ScrapperTwitterDataconfig()
        self.tweet_topic = tweet_topic
        self.tweets = None  # Initialize tweets here

    async def get_Twitter_details(self):
        config = ConfigParser()  # Create a ConfigParser object
        config.read(self.ScrapperTwitterobj.config_path)
        Username = config['first_user']['user'].strip()
        email = config['first_user']['email'].strip()
        password = config['first_user']['password'].strip()
        return Username, email, password

    async def authenticate_twitter_user(self) -> None:
        cookies_path = os.path.join(self.ScrapperTwitterobj.artifact_path, 'cookies.json')
        if os.path.exists(cookies_path):
            try:
                os.remove(cookies_path)
                print(f'Removed old cookies file: {cookies_path}')
            except Exception as e:
                print(f'Failed to delete {cookies_path}. Reason: {e}')
        Username, email, password = await self.get_Twitter_details()
        print("The new username is", Username)
        print("The new email is", email)
        print("Password is", password)
        client = Client('en-US')

        await client.login(
            auth_info_1=Username,
            auth_info_2=email,
            password=password
        )

        client.save_cookies(cookies_path)
        print("Saved new cookies.")

    async def get_tweets(self):
        client = Client('en-US')
        client.load_cookies(os.path.join(self.ScrapperTwitterobj.artifact_path, 'cookies.json'))

        if self.tweets is None:
            print("Searching for tweets...")
            self.tweets = await client.search_tweet(self.tweet_topic, 'Latest', 1)
        else:
            wait_time = randint(5, 10)
            print(f"Waiting for {wait_time} seconds before fetching the next batch.")
            await asyncio.sleep(wait_time)
            self.tweets = await self.tweets.next()  # Get the next batch of tweets
                
        print("Fetched tweets: ", vars(self.tweets))
        return self.tweets

    async def make_twitter_request(self, num_tweets):
        print("The requested number of tweets is", num_tweets)

        tweet_count = 0

        while tweet_count < num_tweets:
            print("the value of tweet count is", tweet_count)
            print('------------------')
            try:
                tweets = await self.get_tweets()  # No need to pass tweets

            except TooManyRequests as e:
                rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
                wait_time = rate_limit_reset - datetime.now()
                await asyncio.sleep(wait_time.total_seconds())
                continue
            if not tweets:
                break        
            for tweet in tweets:
                print("the tweet cpimt os", tweet_count)
                tweet_count += 1
                tweet_data = [tweet_count, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count]

                with open(self.ScrapperTwitterobj.Testing_dataset_path, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(tweet_data)
        
        st.session_state.scraping_finished = True
    


def start_scrapping(tweet_topic, num_tweets):
    try:
        scrapper = ScrapperTwitterData(tweet_topic)
        asyncio.run(scrapper.authenticate_twitter_user())
        asyncio.run(scrapper.make_twitter_request(num_tweets))

    except Exception as e:
        print(f"An error occurred: {e}")
        # Uncomment if you have a custom exception
        # raise CustomException(e, sys) from e



st.title("Twitter Scrapper")
tweet_topic = st.text_input("Enter the topic for tweet scraping")
num_tweets = st.number_input("Enter the number of tweets to scrape (1-100 is suggested)", min_value=1, max_value=100, value=1)

if st.button('Start Scrapping'):
    start_scrapping(tweet_topic, num_tweets)

# Display the upload button only if scraping is finished
if 'scraping_finished' in st.session_state and st.session_state.scraping_finished:
    if st.button('Upload to S3'):
        upload_to_s3()
