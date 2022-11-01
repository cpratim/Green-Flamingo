from flask import Blueprint
from flask_socketio import emit, SocketIO
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
socketio = SocketIO(app)

app.config['SECRET_KEY'] = 'secret!'
main_blueprint = Blueprint('main', __name__, template_folder='')
CORS(app)
