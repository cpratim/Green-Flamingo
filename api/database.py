import json
from pprint import pprint

def refresh_database():
    with open('api/data/tickers.json', 'w') as f:
        trades = []
        data = {
            "ECON": {
                "title": "Wood Duck",
                "art_id": "econ",
                "artist": "Will Johnson",
                "price": 100,
                "quantity": 10,
                "description": "Male Wood Duck on Eastern Cottonwood branch rendered in color pencil on 18” x 24” matte drawing paper. Drawing time: 10 hours.",
                "category": "Econ26 Final Project",
                "volume": 0,
                "transactions": 0,
                "last_trade_price": 100,
                "trades": trades,
                "orderbook": {
                    "bids": [],
                    "asks": []
                }
            }
        }
        json.dump(data, f, indent=4)
    with open('api/data/users.json', 'w') as f:
        json.dump({}, f, indent=4)
    print('Database refreshed')

class Database(object):

    def __init__(self) -> None:
        self.user_file = 'api/data/users.json'
        self.ticker_file = 'api/data/tickers.json'
        self.user_data = self.load_data(self.user_file)
        self.ticker_data = self.load_data(self.ticker_file)

    def refresh_user_data(self):
        with open(self.user_file, 'w') as f:
            json.dump(self.user_data, f, indent=4)
        with open(self.user_file, 'r') as f:
            self.user_data = json.load(f)

    def refresh_ticker_data(self):
        with open(self.ticker_file, 'w') as f:
            json.dump(self.ticker_data, f, indent=4)
        with open(self.ticker_file, 'r') as f:
            self.ticker_data = json.load(f)

    def load_data(self, file):
        with open(file, 'r') as f:
            data = json.load(f)
        return data

    def get_user_data(self, username):
        self.user_data = self.load_data(self.user_file)
        return self.user_data[username]

    def get_all_users(self):
        self.user_data = self.load_data(self.user_file)
        data = {}
        for username in self.user_data:
            quantity = 0
            if 'ECON' in self.user_data[username]['portfolio']:
                quantity = self.user_data[username]['portfolio']['ECON']
            data[username] = {
                'balance': self.user_data[username]['balance'],
                'quantity': quantity
            }
        return data

    def add_user(self, username, init_balance=1000):
        self.user_data = self.load_data(self.user_file)
        if username in self.user_data:
            return False
        self.user_data[username] = {
            'balance': init_balance,
            'active_order': {},
            'history': [],
            'portfolio': {}
        }
        self.refresh_user_data()
        return True

    def get_orderbook(self, orderbook):
        bids = {}
        asks = {}
        for price, quantity, _ in orderbook['bids']:
            if price not in bids:
                bids[price] = 0
            bids[price] += quantity

        for price, quantity, _ in orderbook['asks']:
            if price not in asks:
                asks[price] = 0
            asks[price] += quantity

        orderbook = {'bids': [], 'asks': []}
        for price, quantity in sorted(bids.items(), key=lambda x: x[0], reverse=True):
            orderbook['bids'].append([round(float(price), 2) , quantity])
        for price, quantity in sorted(asks.items(), key=lambda x: x[0]):
            orderbook['asks'].append([round(float(price), 2) , quantity])
        orderbook['bids'] = orderbook['bids'][:5]
        orderbook['asks'] = orderbook['asks'][:5]
        return orderbook

    def get_ticker_data(self, ticker):
        self.ticker_data = self.load_data(self.ticker_file)
        data = {}

        for key in self.ticker_data[ticker]:
            if key not in ['orderbook', 'trades']:
                data[key] = self.ticker_data[ticker][key]
        data['orderbook'] = self.get_orderbook(self.ticker_data[ticker]['orderbook'])
        data['trades'] = self.ticker_data[ticker]['trades'][-250:]
        return data

    def process_order(self, ticker, side, price, quantity, username):
        if side == 'buy':
            transactions, order = self.match_buy(ticker, price, quantity, username)
        else:
            transactions, order = self.match_sell(ticker, price, quantity, username)

        if username in transactions:
            trade_price = abs(round(transactions[username]['total'] / transactions[username]['filled'], 2))
            trade_number = 0 if len(self.ticker_data[ticker]['trades']) == 0 else self.ticker_data[ticker]['trades'][-1][0]
            self.ticker_data[ticker]['trades'].append([trade_number+1, trade_price])
            self.ticker_data[ticker]['last_trade_price'] = trade_price
            self.ticker_data[ticker]['volume'] += abs(transactions[username]['filled'])
        self.refresh_ticker_data()
        return transactions, order

    def process_user_order(self, username, ticker, side, price, quantity):
        self.user_data = self.load_data(self.user_file)
        if side == 'buy':
            if self.user_data[username]['balance'] < price * quantity:
                return False
            if ticker not in self.user_data[username]['portfolio']:
                self.user_data[username]['portfolio'][ticker] = 0
            self.user_data[username]['portfolio'][ticker] += quantity
            self.user_data[username]['balance'] -= price * quantity
        else:
            if ticker not in self.user_data[username]['portfolio'] or self.user_data[username]['portfolio'][ticker] < quantity:
                return False
            self.user_data[username]['portfolio'][ticker] -= quantity
            self.user_data[username]['balance'] += price * quantity
        self.user_data[username]['history'].append({
            'side': 'Buy' if side == 'buy' else 'Sell',
            'price': price,
            'quantity': quantity,
            'type': 'filled',
        })
        trade_number = 0 if len(self.ticker_data[ticker]['trades']) == 0 else self.ticker_data[ticker]['trades'][-1][0]
        self.ticker_data[ticker]['trades'].append([trade_number+1, price])
        self.ticker_data[ticker]['last_trade_price'] = price
        self.ticker_data[ticker]['volume'] += quantity
        self.refresh_ticker_data()
        self.refresh_user_data()
        return True

    def match_buy(self, ticker, price, quantity, username):
        transactions = {}
        order = {}
        orderbook = self.ticker_data[ticker]['orderbook']
        orderbook['asks'] = sorted(orderbook['asks'], key=lambda x: x[0])
        filled = 0
        while orderbook['asks'] and orderbook['asks'][0][0] <= price and filled < quantity:
            if orderbook['asks'][0][1] <= (quantity - filled):
                filled += orderbook['asks'][0][1]
                fill_price, fill_quantity, fill_username = orderbook['asks'].pop(0)
                fill_price = (fill_price + price) / 2
                if fill_username not in transactions:
                    transactions[fill_username] = {
                        'filled': -fill_quantity,
                        'total': price * fill_price,
                    }
                if username not in transactions:
                    transactions[username] = {
                        'filled': 0, 
                        'total': 0,
                    }
                transactions[username]['filled'] += fill_quantity
                transactions[username]['total'] += price * fill_quantity

            else:
                fill_price, fill_quantity, fill_username = orderbook['asks'].pop(0)
                fill_price = (fill_price + price) / 2
                transactions[username] = {
                    'filled': quantity,
                    'total': price * quantity
                }
                transactions[fill_username] = {
                    'filled': -quantity,
                    'total': price * quantity
                }
                if fill_quantity - quantity > 0:
                    orderbook['asks'].insert(0, [fill_price, fill_quantity - quantity, fill_username])
                filled = quantity
        if filled < quantity:
            orderbook['bids'].append([price, quantity - filled, username])
            order = {
                'price': price,
                'quantity': quantity - filled,
                'username': username
            }
        return transactions, order

    def match_sell(self, ticker, price, quantity, username):
        transactions = {}
        order = {}
        orderbook = self.ticker_data[ticker]['orderbook']
        orderbook['bids'] = sorted(orderbook['bids'], key=lambda x: x[0], reverse=True)
        filled = 0
        while orderbook['bids'] and orderbook['bids'][0][0] >= price and filled < quantity:
            if orderbook['bids'][0][1] <= (quantity - filled):
                filled += orderbook['bids'][0][1]
                fill_price, fill_quantity, fill_username = orderbook['bids'].pop(0)
                fill_price = (fill_price + price) / 2
                if fill_username not in transactions:
                    transactions[fill_username] = {
                        'filled': fill_quantity,
                        'total': -price * fill_price,
                    }
                if username not in transactions:
                    transactions[username] = {
                        'filled': 0,
                        'total': 0,
                    }
                transactions[username]['filled'] += fill_quantity
                transactions[username]['total'] += price * fill_quantity

            else:
                fill_price, fill_quantity, fill_username = orderbook['bids'].pop(0)
                fill_price = (fill_price + price) / 2
                transactions[username] = {
                    'filled': -quantity,
                    'total': price * quantity
                }
                transactions[fill_username] = {
                    'filled': quantity,
                    'total': -price * quantity
                }
                if fill_quantity - quantity > 0:
                    orderbook['bids'].insert(0, [fill_price, fill_quantity - quantity, fill_username])
                filled = quantity
        if filled < quantity:
            orderbook['asks'].append([price, quantity - filled, username])
            order = {
                'price': price,
                'quantity': quantity - filled,
                'username': username
            }
        return transactions, order
