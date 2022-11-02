import json
from api.util import (
    hash_password,
    generate_id
)
import datetime


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

    def add_ticker(self, title, ticker, username, art_id, price, quantity, description, category):
        if ticker in self.data['tickers']:
            print('here')
            return None
        if username not in self.data['users']:
            print('here2')
            return None
        if username not in self.data['tickers']:
            self.data['tickers'][username] = {}
        self.data['tickers'][username][ticker] = {
            'title': title,
            'art_id': art_id,
            'price': int(price),
            'quantity': int(quantity),
            'description': description,
            'category': category,
            'volume': 0,
            'transactions': 0,
            'orderbook':  {
                'ask': {
                    price: [
                        {'quantity': int(quantity), 'username': username}
                    ]
                },
                'bid': {}
            },
        }
        if ticker in self.data['users'][username]['active_tickers']:
            return None
        self.data['users'][username]['active_tickers'].append(ticker)
        self.data['users'][username]['portfolio'][f'{username}.{ticker}'] = {
            'quantity': int(quantity),
            'cost': int(price) * int(quantity),
        }
        self.data['users'][username]['active_orders'][f'{username}.{ticker}'] = {
            'quantity': int(quantity),
            'price': int(price),
            'side': 'sell',
            'type': 'limit',
        }
        self.save()
        return ticker

    def get_bids(self, artist, ticker):
        if artist not in self.data['tickers']:
            return None
        if ticker not in self.data['tickers'][artist]:
            return None
        return sorted([
            int(x) for x in self.data['tickers'][artist][ticker]['orderbook']['bid']
        ], reverse=True)

    def get_asks(self, artist, ticker):
        if artist not in self.data['tickers']:
            return None
        if ticker not in self.data['tickers'][artist]:
            return None
        return sorted([
            int(x) for x in self.data['tickers'][artist][ticker]['orderbook']['ask']
        ])

    def get_market_price(self, artist, ticker):
        if artist not in self.data['tickers']:
            return None
        if ticker not in self.data['tickers'][artist]:
            return None
        ask, bid = None, None
        bids, asks = self.get_bids(artist, ticker), self.get_asks(artist, ticker)
        if bids:
            bid = max(bids)
        if asks:
            ask = min(asks)
        if ask is None and bid is None:
            return 0
        if ask is None:
            return bid
        if bid is None:
            return ask
        return (ask + bid) / 2

    def get_orderbook(self, artist, ticker):
        if artist not in self.data['tickers']:
            return None
        if ticker not in self.data['tickers'][artist]:
            return None
        bids = self.get_bids(artist, ticker)
        asks = self.get_asks(artist, ticker)
        orderbook = {'bid': {}, 'ask': {}}
        total = 0
        for price in bids:
            orderbook['bid'][price] = {
                'quantity': 0,
            }
            for order in self.data['tickers'][artist][ticker]['orderbook']['bid'][str(price)]:
                orderbook['bid'][price]['quantity'] += order['quantity']
                total += order['quantity']
        for price in orderbook['bid']:
            percentage = round(orderbook['bid'][price]['quantity'] / total, 2)
            orderbook['bid'][price]['percentage'] = percentage
        
        for price in asks:
            orderbook['ask'][price] = {
                'quantity': 0,
            }
            for order in self.data['tickers'][artist][ticker]['orderbook']['ask'][str(price)]:
                orderbook['ask'][price]['quantity'] += order['quantity']
                total += order['quantity']
        for price in orderbook['ask']:
            percentage = round(orderbook['ask'][price]['quantity'] / total, 2)
            orderbook['ask'][price]['percentage'] = percentage
        return orderbook
            
    def process_transaction(self, username, transaction):
        ticker = transaction['ticker']
        if ticker not in self.data['users'][username]['portfolio']:
            self.data['users'][username]['portfolio'][ticker] = {
                'quantity': 0,
                'cost': 0,
            }
        self.data['users'][username]['portfolio'][ticker]['quantity'] += transaction['quantity']
        self.data['users'][username]['portfolio'][ticker]['cost'] += transaction['cost']
        if self.data['users'][username]['portfolio'][ticker]['quantity'] == 0:
            del self.data['users'][username]['portfolio'][ticker]
        self.data['users'][username]['balance'] -= transaction['cost']

        self.data['users'][username]['active_orders'][f'{username}.{ticker}']['quantity'] -= transaction['quantity']
        if self.data['users'][username]['active_orders'][f'{username}.{ticker}']['quantity'] == 0:
            del self.data['users'][username]['active_orders'][f'{username}.{ticker}']

        self.save()

    def get_position(self, artist, ticker, username):
        if artist not in self.data['tickers']:
            return None
        if ticker not in self.data['tickers'][artist]:
            return None
        if username not in self.data['users']:
            return None
        if f'{artist}.{ticker}' not in self.data['users'][username]['portfolio']:
            return None
        position = self.data['users'][username]['portfolio'][f'{artist}.{ticker}']
        position['market_value'] = self.get_market_price(artist, ticker) * position['quantity']
        position['fill_price'] = round(position['cost'] / position['quantity'], 2)
        position['last_updated'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return position

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
            'active_orders': {},
            'active_tickers': [],
        }
        self.save()
        return True

    def get_portfolio(self, username):
        if username not in self.data['users']:
            return None
        return self.data['users'][username]['portfolio']

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