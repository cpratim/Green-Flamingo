from collections import deque
from heapq import (
    heappop,
    heappush,
    heapify
)


class OrderBook(object):

    def __init__(self):
        self.bids = []
        self.asks = []
        heapify(self.bids)
        heapify(self.asks)

    def add_order(self, order, side):
        if side == 'buy':
            if self.asks and self.asks[0][0] <= order['price']:
                ask = self.execute_order(order, side)
                return {
                    'type': 'match',
                    'fill_price': ask[0],
                }
            else:
                heappush(self.bids, (-order['price'], order['size']))
        else:
            if self.bids and -self.bids[0][0] >= order['price']:
                bid = self.execute_order(order, side)
                return {
                    'type': 'match',
                    'fill_price': -bid[0],
                }
            else:
                heappush(self.asks, (order['price'], order['size']))
        return {
            'type': 'pending',
        }

    def execute_order(self, order, side):
        if side == 'buy':
            return heappop(self.asks)
        else:
            return heappop(self.bids)

    def get_order_book(self):
        return {
            'bids': self.bids,
            'asks': self.asks,
        }
