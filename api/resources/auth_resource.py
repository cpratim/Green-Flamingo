from flask import (
    jsonify,
    request,
)
from flask_restx import Resource, Namespace
from api.database import Database


auth_namespace = Namespace('auth', description='Auth related operations')
database = Database()


@auth_namespace.route('/login')
class LoginResource(Resource):
    
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        if database.authenticate(username, password):
            return jsonify({
                'status': '200',
                'username': username,
            })
        return jsonify({
            'status': '401',
        })
        

@auth_namespace.route('/register')
class RegisterResource(Resource):
        
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']
        username = data['username']
        if database.register_user(username, password, email):
            return jsonify({
                'status': '200',
            })
        return jsonify({
            'status': '401',
        })