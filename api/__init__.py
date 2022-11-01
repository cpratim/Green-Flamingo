from flask import (
    Flask,
)
from flask_cors import CORS
from flask_restx import Api
from api.resources import (
    trade_namespace,
    auth_namespace,
    art_namespace
)


def create_api():
    app = Flask(__name__)
    api = Api(app, version="1.0", title="Backend API")
    api.add_namespace(trade_namespace, path='/api/v1/trade')
    api.add_namespace(auth_namespace, path='/api/v1/auth')
    api.add_namespace(art_namespace, path='/api/v1/art')
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    return app
