#!/usr/bin/env python3

import os
import logging as log

import requests
from dotenv import load_dotenv, find_dotenv

import cat_scraper
import cat_store


def send_message(channel, msg, token):
    response = requests.get(f'https://api.telegram.org/bot{token}/sendMessage?chat_id={channel}&text={msg}')
    if not response.ok:
        log.warning('Response from Telegram not OK. Status: %d, body: %s', response.status_code, response.text)


if __name__ == '__main__':
    log.basicConfig(filename='scraper.log', encoding='utf-8', level=log.INFO, format='%(asctime)s %(levelname)s %(message)s')
    load_dotenv(find_dotenv())

    url = os.environ.get('SCRAPE_URL')
    telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    channel_id = os.environ.get('TELEGRAM_CHAT_ID')

    # Load the already known cats into the store.
    store = cat_store.CatStore('cats.json')

    # Make a scraper and scrape for cats.
    scraper = cat_scraper.CatScraper(url)
    cats = scraper.get_cats()

    # Add the cats to the store.
    store.add(cats)

    # Persist the cats to disk.
    store.save()

    # Notify the channel about new cats.
    for cat in store.get_new_cats():
        log.info('New cat: %s', cat['name'])
        msg = f'There is a new cat called {cat["name"]}! 😻 See {cat["url"]}'
        send_message(channel_id, msg, telegram_token)

