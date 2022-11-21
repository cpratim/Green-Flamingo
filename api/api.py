from flask import Blueprint, request, send_file, jsonify
from api.database import Database
from flask_socketio import SocketIO

database = Database()
socketio = SocketIO()


api_blueprint = Blueprint('api', __name__, url_prefix='/api')


@api_blueprint.route('/<string:ftype>/<string:fname>', methods=['GET'])
def get_file(ftype, fname):
    return send_file(f'static/{ftype}/{fname}')


@api_blueprint.route('/ticker/<string:ticker>', methods=['GET'])
def get_ticker_data(ticker):
    return jsonify(database.get_ticker_data(ticker))


@api_blueprint.route('/user/<string:username>', methods=['GET'])
def get_user_data(username):
    return jsonify(database.get_user_data(username))


@api_blueprint.route('/all_users', methods=['GET'])
def get_all_users():
    return jsonify(database.get_all_users())


# @api_blueprint.route('/order', methods=['POST'])
# def process_order():
#     data = request.get_json()
#     transactions, order = database.process_order(
#         data['ticker'], data['side'], data['price'], data['quantity'], data['username']
#     )
#     socketio.emit('trade', broadcast=True)
#     return jsonify({'transactions': transactions, 'order': order})
