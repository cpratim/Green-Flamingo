import json
from api.util import (
    hash_password,
    generate_id
)


class Database(object):

    def __init__(self, file='api/database/database.json', init=False):
        self.file = file
        self.data = self.load()
        if init:
            self.init()

    def init(self):
        self.data = {
            'auth': {},
            'users': {},
            'tickers': {},
        }
        self.save()

    def load(self):
        with open(self.file, 'r') as f:
            self.data = json.load(f)
        return self.data

    def save(self):
        with open(self.file, 'w') as f:
            json.dump(self.data, f, indent=4)
        self.load()

    def add_ticker(self, title, ticker, username, art_id, price, quantity):
        if ticker in self.data['tickers']:
            return None
        if username not in self.data['users']:
            return None
        if username not in self.data['tickers']:
            self.data['tickers'][username] = {}
        self.data['tickers'][username][ticker] = {
            'title': title,
            'art_id': art_id,
            'price': int(price),
            'quantity': int(quantity),
            'volume': 0,
            'transactions': 0,
            'orderbook':  {},
        }
        if ticker in self.data['users'][username]['active_tickers']:
            return None
        self.data['users'][username]['active_tickers'].append(ticker)
        self.save()
        return ticker

    def get_orderbook(self, artist, ticker):
        if artist not in self.data['tickers']:
            return None
        if ticker not in self.data['tickers'][artist]:
            return None
        return self.data['tickers'][artist][ticker]['orderbook']

    def register_user(self, username, password, email, default_balance=1000):
        if username in self.data['users']:
            return False
        user_id = generate_id(username)
        self.data['auth'][username] = {
            'id': user_id,
            'email': email,
            'password': hash_password(password),
        }
        self.data['users'][username] = {
            'balance': default_balance,
            'portfolio': {},
            'active_tickers': [],
        }
        self.save()
        return True

    def authenticate(self, username, password):
        if username not in self.data['auth']:
            return False
        if self.data['auth'][username]['password'] != hash_password(password):
            return False
        return True

    def get_ticker_data(self, username, ticker):
        if username not in self.data['tickers']:
            return None
        if ticker not in self.data['tickers'][username]:
            return None
        return self.data['tickers'][username][ticker]

    def get_user_id(self, username):
        if username not in self.data['auth']:
            return False
        return self.data['auth'][username]['id']

    def store_temp_image(self, image):
        pass