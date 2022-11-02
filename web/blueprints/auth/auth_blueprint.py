from flask import render_template, request, jsonify, session, redirect, url_for
import requests
from web.blueprints.index.index_blueprint import js
from flask import make_response
from web.config import API_HOST
from web import main_blueprint

templates_dir = 'blueprints/auth/templates'


@main_blueprint.route('/login', methods=['GET'])
def login():
    return render_template(f'{templates_dir}/login.html')


@main_blueprint.route('/register', methods=['GET'])
def register():
    return render_template(f'{templates_dir}/register.html')

@main_blueprint.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('main.login'))


@main_blueprint.route('/login_handler', methods=['POST'])
def login_handler():
    data = request.get_json()
    req = requests.post(f'{API_HOST}/api/v1/auth/login', json=data).json()
    if req['status'] == '200':
        session['logged_in'] = True
        session['username'] = req['username']
        return jsonify({
            'status': '200',
            'username': req['username'],
        })
    return jsonify({
        'status': '401',
    })
