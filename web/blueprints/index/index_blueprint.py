from flask import Blueprint, send_file
from flask_socketio import emit
from flask import render_template
from web import main_blueprint


@main_blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')
    

@main_blueprint.route('/misc/<string:filename>', methods=['GET'])
def misc(filename):
    return send_file('static/misc/' + filename)


@main_blueprint.route('/css/<string:route>/<string:filename>', methods=['GET'])
def css(route, filename):
    if route == 'common':
        return send_file('static/css/' + filename)
    return send_file('blueprints/' + route + '/static/css/' + filename)


@main_blueprint.route('/js/<string:route>/<string:filename>', methods=['GET'])
def js(route, filename):
    if route == 'common':
        return send_file('static/js/' + filename)
    return send_file('blueprints/' + route + '/static/js/' + filename)
