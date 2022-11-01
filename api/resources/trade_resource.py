from flask import (
    jsonify,
    request,
)
from flask_restx import Resource, Namespace
from api import database
from api.database import Database
from api.engine import OrderBook, Stream

stream = Stream()
trade_namespace = Namespace('trade', description='Trade related operations')
database = Database()


@trade_namespace.route('/')
class OrderResource(Resource):

    def post(self):
        order = request.get_json()
        orderbook = OrderBook(order['artist'], order['ticker'])
        status = orderbook.add_order(order, order['side'])
        if status['type'] == 'match':
            stream.stream_trade({
                'price': status['fill_price'],
                'size': order['size'],
            })
        else:
            stream.stream_order(order)
        return jsonify(status)


@trade_namespace.route('/ticker/<string:username>/<string:ticker>')
class TickerResource(Resource):
    
    def get(self, username, ticker):

        data = database.get_ticker_data(username, ticker)
        if data is None:
            return jsonify({
                'error': 'Ticker does not exist',
            })
        return jsonify(data)