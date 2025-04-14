from app import login_manager
from flask_login import UserMixin # Этот класс даёт возможность работать с пользователем
from flask_sqlalchemy import SQLAlchemy

@login_manager.user_loader
def load_user(user_id):
    return Accounts.query.get(int(user_id)) # Эта строчка будет отправлять в БД запрос для поиска определённого юзера по его ID

db = SQLAlchemy()

class Accounts(db.Model, UserMixin):
    __tablename__ = 'accounts'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def get_id(self):
        return str(self.user_id)

    def __repr__(self):  # Функция, чтобы представить информацию о пользователе в виде одной строки
        return f'User: {self.username}, email: {self.emai}'


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    hobby = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<User {self.name}, {self.email}>'