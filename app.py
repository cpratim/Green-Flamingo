from flask import Flask, request, jsonify
from flask_socketio import emit, SocketIO
from api.api import api_blueprint
from web.web import web_blueprint
from flask_socketio import socketio
from api.database import Database, refresh_database
from flask_ngrok import run_with_ngrok

# refresh_database()
database = Database()
socketio = SocketIO()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.register_blueprint(api_blueprint)
app.register_blueprint(web_blueprint)

@socketio.on('connect')
def ping():
    socketio.emit('trade', database.get_ticker_data('ECON'))

@app.route('/api/order', methods=['POST'])
def process_order():
    data = request.get_json()
    transactions, order = database.process_order(
        data['ticker'], data['side'], data['price'], data['quantity'], data['username']
    )
    socketio.emit('trade', database.get_ticker_data('ECON'), broadcast=True)
    return jsonify({'transactions': transactions, 'order': order})

@app.route('/api/user_order', methods=['POST'])
def user_order():
    data = request.get_json()
    side = data['side']
    username = data['username']
    ticker = data['ticker']
    price = data['price']
    quantity = data['quantity']
    try:
        price = float(price)
        quantity = float(quantity)
    except:
        return jsonify({'error': 'Invalid price or quantity'})
    if price <= 0 or quantity <= 0:
        return jsonify({'error': 'Invalid price or quantity'})
    status = database.process_user_order(username, ticker, side, price, quantity)
    if not status:
        return jsonify({'error': 'Invalid order'})
    socketio.emit('trade', database.get_ticker_data('ECON'), broadcast=True)
    return database.get_user_data(username)

@app.route('/api/new_user', methods=['GET'])
def new_user():
    socketio.emit('new_user', database.get_all_users(), broadcast=True)
    return 'ok'
    

socketio.init_app(app)

if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0', port=80)