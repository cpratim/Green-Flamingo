import re
from unicodedata import category
from flask import (
    jsonify,
    request,
    send_file
)
from flask_restx import Resource, Namespace
from api import database
from api.database.database import Database
from api.util import generate_id
from api.database import Database
from pprint import pprint

database = Database()

art_namespace = Namespace('storage', description='Storage related operations')


@art_namespace.route('/upload')
class StorageResource(Resource):

    def post(self):
        image_id = generate_id(str(request.data))
        with open('api/database/blob/' + image_id + '.png', 'wb') as f:
            f.write(request.data)
        return jsonify({'id': image_id})


@art_namespace.route('/<string:id>')
class ArtResource(Resource):
    
    def get(self, id):
        return send_file('database/blob/' + id + '.png')


@art_namespace.route('/submit')
class SubmitResource(Resource):
        
    def post(self):
        data = request.get_json()
        title = data['title']
        username = data['username']
        art_id = data['artID']
        ipo_price = data['ipoPrice']
        ticker = data['ticker']
        quantity = data['quantity']
        description = data['description']
        category = data['category']
        try:
            int(ipo_price)
            int(quantity)
        except ValueError:
            return jsonify({'status': 'failed'})
        if int(ipo_price) <= 0 or int(quantity) <= 0 or len(ticker) > 5 or len(ticker) < 1:
            return jsonify({'status': 'failed'})
        ticker = database.add_ticker(title, ticker, username, art_id, ipo_price, quantity, description, category)
        if not ticker:
            return jsonify({'status': 'failed'})
        return jsonify({
            'status': 'success',
            'ticker': ticker,
        })