from flask import Blueprint
from flask_socketio import emit
from flask import request


trade_blueprint = Blueprint('trade', __name__)


@trade_blueprint.route('/trade', methods=['GET'])
def trade():
    json = request.get_json()
    emit('trade', json, broadcast=True)
    return 'OK'


@trade_blueprint.route('/order', methods=['GET'])
def order():
    json = request.get_json()
    emit('order', json, broadcast=True)
