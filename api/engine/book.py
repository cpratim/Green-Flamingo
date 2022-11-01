from collections import deque
from heapq import (
    heappop,
    heappush,
    heapify
)
from api import database
from api.database import Database


database = Database()


class OrderBook(object):

    def __init__(self, artist, ticker):
        self.orderbook = database.get_orderbook(artist, ticker)

    def add_order(self, order):
        max_buy = max(self.orderbook['buy'].keys())
        min_sell = min(self.orderbook['sell'].keys())
        side = order['side']
        if side == 'buy' and order['price'] >= min_sell:
            return self.match(side, order, min_sell)
        elif side == 'sell' and order['price'] <= max_buy:
            return self.match(side, order, max_buy)
        return {
            'type': 'add',
            'order': order,
        }

    def match(self, side, order, fill_price):
        if side == 'buy':
            latest = self.orderbook['sell'][fill_price].pop(0)
            return {
                'type': 'match',
                'fill_price': fill_price,
            }
        else:
            latest = self.orderbook['buy'][fill_price].pop(0)
            return {
                'type': 'match',
                'fill_price': fill_price,
            }
        