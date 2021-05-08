#!/usr/bin/env python3

import argparse
from urllib.parse import urlsplit
import requests
from bs4 import BeautifulSoup
import json

def div_to_cat(cat_div):
    return {
        'url': base_path + cat_div.find('a')['href'],
        'name': cat_div.find('li', class_='naam').text.split(':')[1],
        'status': cat_div.find('li', class_='status').text.split(':')[1],
    }


def get_cats(url):
    response = requests.get(url)
    if not response.ok:
        print(f'Unsuccessful request to {url}. Giving up.')
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    # Select all <div> elements with a 'dieren' class, but WITHOUT the 'header'
    # class.
    cat_divs = soup.select('div.dieren:not(.header)')

    # Convert the <div> elements to cat dictionaries.
    cats = [div_to_cat(cat_div) for cat_div in cat_divs]
    return cats


def save_cats(cats):
    new_cats = []
    stored_cats = dict()
    try:
        with open('./cats.json') as cat_file:
            stored_cats = json.load(cat_file)
            for cat in cats:
                if cat['url'] not in stored_cats:
                    # This is a new cat!
                    new_cats.append(cat)
                    stored_cats[cat['url']] = cat
    except FileNotFoundError:
        # All cats are new
        new_cats = cats
        # We need to store all of them
        for cat in cats:
            stored_cats[cat['url']] = cat

    # Save the cats.
    with open('./cats.json', 'w') as cat_file:
        json.dump(stored_cats, cat_file, indent=2)

    return new_cats


def send_message(channel, msg, token):
    response = requests.get(f'https://api.telegram.org/bot{token}/sendMessage?chat_id={channel}&text={msg}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('telegram_token')
    parser.add_argument('channel_id')
    args = parser.parse_args()

    split_url = urlsplit(args.url)
    base_path = f'{split_url.scheme}://{split_url.netloc}'

    cats = get_cats(args.url)
    new_cats = save_cats(cats)
    for cat in new_cats:
        msg = f'There is a new cat called {cat["name"]}! See {cat["url"]}'
        print(msg)
        send_message(args.channel_id, msg, args.telegram_token)
