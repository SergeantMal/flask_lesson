from flask import Flask, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config
from app.models import db, Accounts
from app.database import create_users_table
from app.routes import routes

# создаём экземпляры
app = Flask(__name__)
app.config.from_object(Config)

# register blueprint
app.register_blueprint(routes)

bcrypt = Bcrypt(app)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Пожалуйста, войдите, чтобы получить доступ к этой странице."
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    return Accounts.query.get(int(user_id))  # Используем ID пользователя для загрузки

@app.errorhandler(401)
def unauthorized(e):
    flash("Пожалуйста, войдите, чтобы получить доступ к этой странице.", "warning")
    return redirect(url_for('login'))

create_users_table()

# ВАЖНО: импорт маршрутов только после создания app и login_manager
from app import routes

# экспортируем переменные, чтобы они были доступны при `from app import app, db, login_manager`
__all__ = ['app', 'db', 'login_manager', 'bcrypt']
