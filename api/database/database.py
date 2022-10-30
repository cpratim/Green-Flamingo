import json
from api.util import (
    hash_password,
    generate_id
)


class Database(object):

    def __init__(self, file='api/database/database.json'):
        self.file = file
        self.data = self.load()

    def load(self):
        with open(self.file, 'r') as f:
            self.data = json.load(f)
        return self.data

    def save(self):
        with open(self.file, 'w') as f:
            json.dump(self.data, f)
        self.load()

    def add_ticker(self, ticker, artist, url, price):
        if ticker in self.data['tickers']:
            return False
        self.data['tickers'][ticker] = {
            'id': generate_id(ticker),
            'artist': artist,
            'url': url,
            'price': price,
            'orderbook':  {},
        }
        self.save()
        return True

    def add_user(self, username, password, default_balance=1000):
        if username in self.data['users']:
            return False
        self.data['users'][username] = {
            'id': generate_id(username),
            'password': hash_password(password),
            'balance': default_balance,
        }
        self.save()
        return True
