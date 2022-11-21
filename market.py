from api.database import Database
from time import sleep
from random import randint, uniform
import requests

#ticker, side, price, quantity, username
url = 'http://127.0.0.1:5500/api/order'


def make_market():
    switch = False
    delta = .15
    base = 100
    step = 0
    spread = 1.5
    min_price = 25
    switch_percentage = 10
    while True:
        price = base + uniform(-spread, spread) + step * delta
        quantity = randint(1, 10)
        if switch:
            print(f'BUY | {price}')
            requests.post(url, json={
                'ticker': 'ECON',
                'side': 'buy',
                'price': price,
                'quantity': quantity,
                'username': 'bot'
            })
        else:
            print(f'SELL | {price}')
            requests.post(url, json={
                'ticker': 'ECON',
                'side': 'sell',
                'price': price,
                'quantity': quantity,
                'username': 'bot2'
            })
        switch = not switch
        sleep(.1)

        step += 1
        if uniform(0, 100) < switch_percentage:
            
            delta = -delta
            step = 0
            base = price

        if price < min_price:
            delta = abs(delta)
            step = 0
            base = price


if __name__ == '__main__':
    make_market()
    # database = Database()

    # database.process_order('ECON', 'buy', 100, 10, 'bot')
    # database.process_order('ECON', 'sell', 90, 15, 'bot')
    # print(database.ticker_data['ECON']['orderbook'])