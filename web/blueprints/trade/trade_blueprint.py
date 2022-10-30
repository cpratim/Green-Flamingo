from flask import Blueprint, render_template
from flask_socketio import emit
from flask import request


trade_blueprint = Blueprint('trade', __name__, template_folder='templates')


@trade_blueprint.route('/place_trade', methods=['POST'])
def place_trade():
    json = request.get_json()
    emit('trade', json, broadcast=True)
    return '200'


@trade_blueprint.route('/place_order', methods=['POST'])
def order():
    json = request.get_json()
    emit('order', json, broadcast=True)
    return '200'


@trade_blueprint.route('/trade', methods=['GET'])
def trade():
    return render_template('trade.html')


@trade_blueprint.route('/asset/<string:id>', methods=['GET'])
def asset():
    return render_template('trade.html')


@trade_blueprint.route('/create', methods=['GET'])
def create():
    return render_template('create.html')