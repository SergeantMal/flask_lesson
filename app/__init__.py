from flask import Flask, redirect, url_for, flash
from app.db import create_users_table
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Пожалуйста, войдите, чтобы получить доступ к этой странице."
login_manager.login_message_category = "warning"



# Обработка попытки доступа к защищённой странице без авторизации
@login_manager.unauthorized_handler
def unauthorized():
    flash("Пожалуйста, войдите, чтобы получить доступ к этой странице.", "warning")
    return redirect(url_for('login'))

from config import Config
from app.models import db


app.config.from_object(Config)

db.init_app(app)

create_users_table()

from app import routes

