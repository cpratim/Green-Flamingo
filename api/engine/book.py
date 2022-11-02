from pprint import pprint
from math import floor


class OrderBook(object):

    def __init__(self, artist, ticker):
        # self.orderbook = database.get_orderbook(artist, ticker)
        # self.bids = self.orderbook['bids']
        # self.asks = self.orderbook['asks']
        self.bids = {}
        self.asks = {}

    def print_orderbook(self):
        print('Bids:')
        for price in sorted(list(self.bids.keys()), reverse=True):
            print(price, self.bids[price])

        print('Asks:')
        for price in sorted(list(self.asks.keys())):
            print(price, self.asks[price])

    def add_order(self, order):
        order_type = order['type']
        side = order['side']
        del order['side']
        del order['type']
        if side == 'buy':
            return self.match_buy_limit(order)
        return self.match_sell(order)

    def match_buy_limit(self, order):
        order_price = order['price']
        del order['price']
        username = order['username']
        quantity = order['quantity']
        spread = sorted(list(self.asks.keys()))
        transactions = {}
        while spread and quantity > 0:
            sell_price = spread.pop(0)
            if sell_price <= order_price:
                while self.asks[sell_price]:
                    sell_order = self.asks[sell_price].pop()
                    sell_user = sell_order['username']
                    fill_amount = min(sell_order['quantity'], quantity)
                    sell_order['quantity'] -= fill_amount
                    if username not in transactions:
                        transactions[username] = {'amount': 0, 'shares': 0}
                    if sell_user not in transactions:
                        transactions[sell_user] = {'amount': 0, 'shares': 0}
                    
                    transactions[username]['amount'] -= fill_amount * sell_price
                    transactions[sell_user]['amount'] += fill_amount * sell_price
                    transactions[username]['shares'] += fill_amount
                    transactions[sell_user]['shares'] -= fill_amount

                    quantity -= fill_amount
                    
                    if sell_order['quantity'] > 0:
                        self.asks[sell_price].insert(0, sell_order)
                    if quantity == 0:
                        break
            if len(self.asks[sell_price]) == 0:
                del self.asks[sell_price]
            if quantity == 0:
                break
        if quantity > 0:
            order['quantity'] = quantity
            if order_price not in self.bids:
                self.bids[order_price] = []
            self.bids[order_price].append(order)
        return transactions

    def match_sell(self, order):
        order_price = order['price']
        username = order['username']
        del order['price']
        quantity = order['quantity']
        spread = sorted(list(self.bids.keys()), reverse=True)
        transactions = {}

        while spread and quantity > 0:
            buy_price = spread.pop(0)
            if buy_price >= order_price:
                while self.bids[buy_price]:
                    
                    buy_order = self.bids[buy_price].pop()
                    buy_user = buy_order['username']
                    fill_amount = min(buy_order['quantity'], quantity)
                    buy_order['quantity'] -= fill_amount
                    quantity -= fill_amount
                    if username not in transactions:
                        transactions[username] = {'amount': 0, 'shares': 0}
                    if sell_user not in transactions:
                        transactions[buy_user] = {'amount': 0, 'shares': 0}
                    
                    transactions[username]['amount'] -= fill_amount * sell_price
                    transactions[buy_user]['amount'] += fill_amount * sell_price
                    transactions[username]['shares'] += fill_amount
                    transactions[buy_user]['shares'] -= fill_amount

                    if buy_order['quantity'] > 0:
                        self.bids[buy_price].insert(0, buy_order)
                    if quantity == 0:
                        break
            if len(self.bids[buy_price]) == 0:
                del self.bids[buy_price]
            if quantity == 0:
                break
        if quantity > 0:
            order['quantity'] = quantity
            if order_price not in self.asks:
                self.asks[order_price] = []
            self.asks[order_price].append(order)
        return transactions

    def match_buy_market(self, order):
        spread = sorted(list(self.asks.keys()))
        transactions = {}
        username = order['username']
        cash = order['cash']
        while spread and cash > 0:
            sell_price = spread.pop(0)
            while self.asks[sell_price]:
                sell_order = self.asks[sell_price].pop()
                
                sell_user = sell_order['username']
                fill_amount = min(sell_order['quantity'], floor(cash / sell_price))
                if floor(cash / sell_price) == 0:
                    cash = 0
                sell_order['quantity'] -= fill_amount
                cash -= fill_amount * sell_price
                if username not in transactions:
                    transactions[username] = {'amount': 0, 'shares': 0}
                if sell_user not in transactions:
                    transactions[sell_user] = {'amount': 0, 'shares': 0}
                
                transactions[username]['amount'] -= fill_amount * sell_price
                transactions[sell_user]['amount'] += fill_amount * sell_price
                transactions[username]['shares'] += fill_amount
                transactions[sell_user]['shares'] -= fill_amount
                
                if sell_order['quantity'] > 0:
                    self.asks[sell_price].append(sell_order)
                if cash == 0:
                    break

            if len(self.asks[sell_price]) == 0:
                del self.asks[sell_price]
            if cash == 0:
                break
        return transactions
                        
                    
if __name__ == '__main__':
    orderbook = OrderBook('test', 'test')
    orderbook.add_order({'side': 'buy', 'price': 5, 'quantity': 10, 'username': 'cpratim', 'type': 'limit'})
    orderbook.add_order({'side': 'buy', 'price': 12.5, 'quantity': 3, 'username': 'user1', 'type': 'limit'})
    
    orderbook.add_order({'side': 'sell', 'price': 14, 'quantity': 5, 'username': 'user2', 'type': 'limit'})
    orderbook.add_order({'side': 'sell', 'price': 15, 'quantity': 10, 'username': 'user4', 'type': 'limit'})
    orderbook.print_orderbook()
    print('------------------')
    transactions = orderbook.add_order({'side': 'buy', 'cash': 50, 'quantity': 15, 'username': 'user3', 'type': 'market'})
    pprint(transactions)
    print('------------------')
    orderbook.print_orderbook()

    
                
