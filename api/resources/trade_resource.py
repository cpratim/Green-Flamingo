from flask import (
    jsonify,
    request,
)
from flask_restx import Resource, Namespace
from api.engine import OrderBook, Stream

order_book = OrderBook()
stream = Stream()
trade_namespace = Namespace('trade', description='Trade related operations')


@trade_namespace.route('/')
class TradeResource(Resource):

    def post(self):
        order = request.get_json()
        status = order_book.add_order(order, order['side'])
        if status['type'] == 'match':
            stream.stream_trade({
                'price': status['fill_price'],
                'size': order['size'],
            })
        else:
            stream.stream_order(order)
        return jsonify(status)
