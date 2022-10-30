from flask import render_template
from flask import Blueprint


auth_blueprint = Blueprint('index', __name__, template_folder='templates')


@auth_blueprint.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@auth_blueprint.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


