from flask import (
    Flask,
)
from flask_restx import Api
from api.resources import (
    trade_namespace
)


def create_api():
    app = Flask(__name__)
    api = Api(app, version="1.0", title="Backend API")
    api.add_namespace(trade_namespace, path='/api/v1/trade')
    return app
