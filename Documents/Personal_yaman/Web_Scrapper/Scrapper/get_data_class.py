from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import yaml
import numpy as np
import pickle
from Final_scrapper import Final_Scrapper

class get_data_class_url_file_config:
    def __init__(self,url):
          self.new_url = url
          self.config_data = self.get_config_Full_file()
          self.get_user_input = self.get_submitted_data()
          self.Final_Scrapper = Final_Scrapper(self.config_data, self.get_user_input,self.new_url)
          
    def get_submitted_data(self):
        with open("submitted_data.pkl", "rb") as f:
            submitted_data = pickle.load(f)
        return submitted_data

    def get_config_Full_file(self):
        module_dir = os.path.dirname(__file__)
        config_path = os.path.join(os.path.dirname(module_dir), 'config.yaml')
        with open(config_path, 'r') as file:
          config_file_data = yaml.safe_load(file)
        return config_file_data

    
    """def scrape_website(self):
        config_data = self.get_config_Full_file()
        headers = config_data['User_agent']
        
        HEADERS = ({'User-Agent': headers, 'Accept-Language': 'en-US, en;q=0.5'})
        webpage = requests.get(self.new_url, headers=HEADERS)
        if webpage.status_code == 200:
            soup = BeautifulSoup(webpage.content, 'html.parser')
        else:
            return f"Error: {webpage.status_code}"

        links = soup.find_all("a", attrs={'class': 'a-link-normal s-no-outline'})

        # Store the links
        links_list = []

        # Loop for extracting links from Tag Objects
        for link in links:
            links_list.append(link.get('href'))

        d = {"title": [], "price": [], "rating": [], "reviews": [], "availability": []}

        for link in links_list:
            new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)
            new_soup = BeautifulSoup(new_webpage.content, "html.parser")

            # Function calls to display all necessary product information
            d['title'].append(self.get_title(new_soup))
            d['price'].append(self.get_price(new_soup))
            d['rating'].append(self.get_rating(new_soup))
            d['reviews'].append(self.get_review_count(new_soup))
            d['availability'].append(self.get_availability(new_soup))

        amazon_df = pd.DataFrame.from_dict(d)
        amazon_df['title'].replace('', np.nan, inplace=True)
        amazon_df = amazon_df.dropna(subset=['title'])
        amazon_df.to_csv("amazon_data.csv", header=True, index=False)


    def get_title(self, soup):
        try:
            # Outer Tag Object
            title = soup.find("span", attrs={"id": 'productTitle'})

            # Inner NavigatableString Object
            title_value = title.text

            # Title as a string value
            title_string = title_value.strip()

        except AttributeError:
            title_string = ""

        return title_string

    # Function to extract Product Price
    def get_price(self, soup):
        try:
            price = soup.find("span", attrs={'id': 'priceblock_ourprice'}).string.strip()
        except AttributeError:
            try:
                # If there is some deal price
                price = soup.find("span", attrs={'id': 'priceblock_dealprice'}).string.strip()
            except:
                price = ""

        return price

    # Function to extract Product Rating
    def get_rating(self, soup):
        try:
            rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()
        except AttributeError:
            try:
                rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()
            except:
                rating = ""

        return rating

    # Function to extract Number of User Reviews
    def get_review_count(self, soup):
        try:
            review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).string.strip()
        except AttributeError:
            review_count = ""

        return review_count

    # Function to extract Availability Status
    def get_availability(self, soup):
        try:
            available = soup.find("div", attrs={'id': 'availability'})
            available = available.find("span").string.strip()
        except AttributeError:
            available = "Not Available"

        return available
"""
    