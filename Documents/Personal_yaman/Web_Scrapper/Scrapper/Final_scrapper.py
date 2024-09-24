from bs4 import BeautifulSoup
import requests

class Final_Scrapper:
    def __init__(self, config_data, user_input, user_url):
        self.config_data = config_data
        self.user_input = user_input
        self.user_url = user_url
        print("The final config_data:", self.config_data)
        print("The user input data is:", self.user_input)
        print("The user URL is:", self.user_url)

        self.scrape_website(self.config_data, self.user_input, self.user_url)

    def scrape_website(self, config_data, user_input, user_url):
        response = requests.get(user_url)
        soup = BeautifulSoup(response.content, "html.parser")
        labels = []
        tags = []

        for key, value in user_input.items():
            labels.append(value['label'])
            tags.append(value['tag'])

        print('The labels are:', labels)
        print('The tags are:', tags)
        
        links = soup.find_all(labels[0], attrs={tags[0]})
        print("the fuull links",links[0])  # Print the first link found

        