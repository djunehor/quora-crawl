"""Module for scraping"""
from bs4 import BeautifulSoup
import dateparser
import datetime


class Scraper:
    """Scraper class"""

    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(html, "lxml")
        print(f"[Scraper] Retrieved page")

    def get_urls(self):
        """Scrapes posts on a page"""
        all_urls = []
        # infinite scroll
        urls = self.soup.find_all("a", class_="SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE")
        for url in urls:
            all_urls.append(url['href'])

        return all_urls

		
    def get_details(self):
        data = {}
        thread = self.soup.find_all('div', 'pagedlist_item')
        user_div = thread.pop()

        a = user_div.find('a', class_="user")
        data['text'] = self.soup.find('span', class_='rendered_qtext').get_text()
        data['user'] = {}
        data['user']['url'] = "https://quora.com"+a['href']
        data['user']['name'] = a.get_text()

        try:
            text = self.soup.find('p', class_="log_action_bar").get_text()
            split = text.split(' · ')
            date_time = split.pop().rstrip()
            data['datetime'] = str(dateparser.parse(date_time))
        except:
            data['datetime'] = str(datetime.datetime.now())

        return data

    def get_followers(self):
        links = self.soup.find_all("span", class_='list_count')
        span = links.pop()
        return span.text
