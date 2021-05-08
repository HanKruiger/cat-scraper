import logging as log
import requests

class TelegramBot:
    def __init__(self, token, channel_id):
        self.token = token
        self.channel_id = channel_id

    def send_message(self, msg):
        response = requests.get(f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.channel_id}&text={msg}')
        if not response.ok:
            log.warning('Response from Telegram not OK. Status: %d, body: %s', response.status_code, response.text)
