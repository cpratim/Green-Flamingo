from http import server
from tabnanny import verbose
from api import create_api
from threading import Thread
from web import app, socketio
from web.blueprints import main_blueprint
import sys
import os

APP_PORT = 5000
API_PORT = 5100


def count_lines():
    lines, n_files = 0, 0
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith('.py') or file.endswith('.html') or file.endswith('.js') or file.endswith('.css'):
                n_files += 1
                with open(os.path.join(root, file), 'r') as f:
                    lines += len([line for line in f.readlines() if line.strip() != ''])
    return lines, n_files


api = create_api()

def run_api():
    api.run(port=API_PORT)


def run_app():
    app.register_blueprint(main_blueprint)
    socketio.run(app)


if __name__ == '__main__':
    server_type = sys.argv[1]
    if server_type == '1':
        run_api()
    elif server_type == '2':
        run_app()
    else:
        lines, files = count_lines()
        print(f'Lines: {lines}, Files: {files}')