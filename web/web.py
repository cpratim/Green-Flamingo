from api.database import Database
from flask import redirect, url_for, session, Blueprint, request, render_template, jsonify
from functools import wraps
from flask_socketio import emit
import requests


TICKER = 'ECON'


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('web.login'))
    return wrap


database = Database()
web_blueprint = Blueprint('web', __name__, url_prefix='/', template_folder='web/templates')

@web_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('web.index'))

@web_blueprint.route('/trade')
@login_required
def trade():
    
    ticker_data = database.get_ticker_data(TICKER)
    try:
        user_data = database.get_user_data(session['username'])
    except:
        session.clear()
        return redirect(url_for('web.index'))
    return render_template(
        'trade.html', 
        ticker_data=ticker_data, 
        username=session['username'],
        user_data=user_data,
        ticker=TICKER,
    )

@web_blueprint.route('/')
def index():
    return render_template('index.html')

@web_blueprint.route('/create')
def create():
    return render_template('create.html')


@web_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.get_json()['username']
        if database.add_user(username):
            session['logged_in'] = True
            session['username'] = username
            return jsonify({'status': '200'})
        return jsonify({'status': '400'})
    return render_template('user.html')


@web_blueprint.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')