import json
from api.util import (
    hash_password,
    generate_id
)


class Database(object):

    def __init__(self, file='api/database/database.json'):
        self.file = file
        self.data = self.load()

    def load(self):
        with open(self.file, 'r') as f:
            self.data = json.load(f)
        return self.data

    def save(self):
        with open(self.file, 'w') as f:
            json.dump(self.data, f)
        self.load()

    def populate(self):
        self.data = {
            'order_book': {
                'bids': [],
                'asks': [],
            },
            'trades': [],
            'users': {},
        }
        self.save()

    def add_user(self, username, password):
        if username in self.data['users']:
            return False
        self.data['users'][username] = {
            'id': generate_id(username),
            'password': hash_password(password),
            'balance': 10000,
        }
        self.save()
        return True
