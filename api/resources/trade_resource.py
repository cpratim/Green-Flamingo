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


@trade_namespace.route('/portfolio/<string:username>')
class PortfolioResource(Resource):
        
    def get(self, username):
        data = database.get_portfolio(username)
        if data is None:
            return jsonify({
                'error': 'User does not exist',
            })
        return jsonify(data)

@trade_namespace.route('/position/<string:username>/<string:artist>/<string:ticker>')
class PositionResource(Resource):
        
    def get(self, username, artist, ticker):
        data = database.get_position(artist, ticker, username)
        if data is None:
            return jsonify({
                'empty': '400',
            })
        return jsonify(data)

@trade_namespace.route('/orderbook/<string:artist>/<string:ticker>')
class OrderBookResource(Resource):
            
    def get(self, artist, ticker):
        data = database.get_orderbook(artist, ticker)
        if data is None:
            return jsonify({
                'empty': '400',
            })
        return jsonify(data)