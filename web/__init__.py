from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from web.blueprints import (
    trade_blueprint,
    index_blueprint,
)


def create_app():
    app = Flask(__name__)
    app.register_blueprint(trade_blueprint)
    app.register_blueprint(index_blueprint)
    socketio = SocketIO(app)
    CORS(app)
    return socketio
