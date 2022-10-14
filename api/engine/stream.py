import requests


class Stream(object):

    def __init__(self):
        self.base = 'http://127.0.0.1:5000'

    def stream_order(self, order):
        return requests.post(self.base + '/order', json=order)

    def stream_trade(self, trade):
        return requests.post(self.base + '/trade', json=trade)
