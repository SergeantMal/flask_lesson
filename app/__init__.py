from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = 'abrakadabra is abrakadabra'

from app import routes
