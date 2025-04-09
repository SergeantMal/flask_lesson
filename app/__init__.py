from flask import Flask
from app.db import create_users_table

app = Flask(__name__)

from app import routes

app.config['SECRET_KEY'] = 'abrakadabra is abrakadabra'

create_users_table()

