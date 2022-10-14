from api import create_api
from web import create_app
from threading import Thread

api = create_api()
app = create_app()


def run_api():
    api.run()


def run_app():
    app.run()


if __name__ == '__main__':
    Thread(target=run_api).start()
    Thread(target=run_app).start()