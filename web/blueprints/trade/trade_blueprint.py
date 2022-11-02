from flask import Blueprint, render_template
from flask import request, session
from web import main_blueprint, socketio
from web.wrappers import login_required
from flask_socketio import emit
import requests
from web.config import API_HOST


templates_dir = 'blueprints/trade/templates'


@main_blueprint.route('/place_trade', methods=['POST'])
def place_trade():
    json = request.get_json()
    emit('trade', json, broadcast=True)
    return '200'


@main_blueprint.route('/place_order', methods=['POST'])
def order():
    json = request.get_json()
    emit('order', json, broadcast=True)
    return '200'


@main_blueprint.route('/test', methods=['GET'])
def test():
    return render_template('macros/navbar.html')


@main_blueprint.route('/trade/<string:artist>/<string:ticker>', methods=['GET'])
@login_required
def trade(artist, ticker):
    username = session['username']
    ticker_data = requests.get(API_HOST + f'/api/v1/trade/ticker/{artist}/{ticker}').json()
    position_data = requests.get(API_HOST + f'/api/v1/trade/position/{username}/{artist}/{ticker}').json()
    orderbook = requests.get(API_HOST + f'/api/v1/trade/orderbook/{artist}/{ticker}').json()
    return render_template(
        f'{templates_dir}/trade.html', 
        ticker_data=ticker_data, 
        position_data=position_data,
        orderbook=orderbook,
    )


@main_blueprint.route('/create', methods=['GET'])
@login_required
def create():
    return render_template(f'{templates_dir}/create.html', username=session['username'])


@socketio.on('upload')
def image_upload_handler(image):
    response = requests.post(f'{API_HOST}/api/v1/art/upload', data=image)
    emit('upload', response.json()['id'], broadcast=True)