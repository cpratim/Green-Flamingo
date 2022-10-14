from flask import Blueprint
from flask_socketio import emit
from flask import render_template


index_blueprint = Blueprint('index', __name__)


@index_blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')
