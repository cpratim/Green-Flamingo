from random import randint
import hashlib


def hash_password(password):
    hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
    return hashed_password


def generate_id(string):
    id = hashlib.sha512(string.encode('utf-8')).hexdigest()
    return id

