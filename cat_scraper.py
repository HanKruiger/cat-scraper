import logging as log
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit

class CatScraper:

    def __init__(self, url):
        self.url = url
        split_url = urlsplit(url)
        self.base_path = f'{split_url.scheme}://{split_url.netloc}'
        self.cats = None

    def scrape(self):
        log.info('Scraping %s', self.url)
        try:
            response = requests.get(self.url)
            if not response.ok:
                log.warning('Response to %s not OK: %s', self.url, response)
                return []
        except requests.exceptions.ConnectionError:
            log.warning('Could not connect to %s', self.url)
            return []

        soup = BeautifulSoup(response.content, 'html.parser')

        # Select all <div> elements with a 'dieren' class, but WITHOUT the
        # 'header' class.
        cat_divs = soup.select('div.dieren:not(.header)')

        # Convert the <div> elements to cat dictionaries.
        self.cats = [self.div_to_cat(cat_div) for cat_div in cat_divs]

    def get_cats(self):
        if self.cats is None:
            self.scrape()
        return self.cats

    def div_to_cat(self, cat_div):
        return {
            'url': self.base_path + cat_div.find('a')['href'],
            'name': cat_div.find('li', class_='naam').text.split(':')[1],
            'status': cat_div.find('li', class_='status').text.split(':')[1],
        }
