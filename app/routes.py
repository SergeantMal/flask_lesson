from flask import render_template, jsonify, redirect, url_for, request, flash
from datetime import datetime
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.db import save_user, load_users, check_email_exists
from app import app, login_manager
from app.models import db
from app.forms import RegisterForm, LoginForm

MONTHS_RU = {
    1: "января", 2: "февраля", 3: "марта", 4: "апреля",
    5: "мая", 6: "июня", 7: "июля", 8: "августа",
    9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
}

pages = {
    "index.html": "Урок <strong>VD07</strong>",
    "blog.html": "<strong>Блог</strong>",
    "contacts.html": "<strong>Контакты</strong>",
    "form.html": "<strong>Анкета пользователя</strong>",
    "account.html": "<strong>Личный кабинет</strong>",
    "register.html": "<strong>Регистрация</strong>",
    "login.html": "<strong>Вход</strong>",
    "edit_account.html": "<strong>Редактирование профиля</strong>"
}


@login_manager.user_loader
def load_user(user_id):
    return Accounts.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html', title=pages['index.html'])

@app.route('/blog/')
def about():
    return render_template('blog.html', title=pages['blog.html'])

@app.route('/contacts/')
def contact():
    return render_template('contacts.html', title=pages['contacts.html'])

@app.route('/time')
def get_time():
    now = datetime.now()
    formatted_date = f"{now.day} {MONTHS_RU[now.month]} {now.year}"
    return jsonify({
        "time": now.strftime("%H:%M:%S"),
        "date": formatted_date
    })


@app.route('/form/', methods=["GET", "POST"])
def form():
    if request.method == "POST":
        user_data = {
            'name': request.form['name'],
            'email': request.form['email'],
            'city': request.form['city'],
            'hobby': request.form['hobby'],
            'age': request.form['age']
        }

        if all(user_data.values()):
            if check_email_exists(user_data['email']):
                flash('Этот email уже зарегистрирован.', 'error')
                return render_template('form.html', title=pages['form.html'], user_data=user_data)
            else:
                save_user(user_data)
                flash('Пользователь успешно добавлен!', 'success')
                return redirect(url_for('form'))

    users = load_users()
    user_data = {'name': '', 'email': '', 'city': '', 'hobby': '', 'age': ''}
    return render_template('form.html', title=pages['form.html'], users=users, user_data=user_data)


# Регистрация
from flask import flash, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash
from app.models import User, Accounts  # убедись, что путь к User правильный


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Проверка на существование пользователя
        existing_user = Accounts.query.filter(
            (Accounts.username == form.username.data) | (Accounts.email == form.email.data)
        ).first()

        if existing_user:
            if existing_user.username == form.username.data:
                flash('Имя пользователя уже занято', 'danger')
            if existing_user.email == form.email.data:
                flash('Email уже зарегистрирован', 'danger')
            return render_template('register.html', form=form, title=pages['register.html'])  # Вернёт обратно форму
        else:
            hashed_password = generate_password_hash(form.password.data)
            user = Accounts(
                username=form.username.data,
                email=form.email.data,
                password=hashed_password
            )
            db.session.add(user)
            db.session.commit()
            flash('Регистрация прошла успешно. Теперь вы можете войти.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form, title=pages['register.html'])


# Авторизация
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Accounts.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Вы вошли в систему!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Неверный логин или пароль', 'danger')
    return render_template('login.html', form=form, title=pages['login.html'])

# Личный кабинет (доступен только авторизованным)
@app.route('/account')
@login_required
def dashboard():
    account = Accounts.query.get(current_user.user_id)
    user = User.query.filter_by(email=account.email).first()
    return render_template('account.html', account=account, user=user, title=pages['account.html'])


@app.route('/account/edit', methods=['GET', 'POST'])
@login_required
def edit_account():
    account = Accounts.query.get(current_user.user_id)
    user = User.query.filter_by(email=account.email).first()

    if request.method == 'POST':
        new_name = request.form['name']
        new_email = request.form['email']
        new_password = request.form['password']
        city = request.form['city']
        age = request.form['age']
        hobby = request.form['hobby']

        # Проверка email
        if Accounts.query.filter(Accounts.email == new_email, Accounts.user_id != account.user_id).first():
            flash('Этот email уже занят другим пользователем.', 'danger')
            return redirect(url_for('edit_account'))

        account.email = new_email
        if new_password:
            account.password = generate_password_hash(new_password)

        user.name = new_name
        user.email = new_email
        user.city = city
        user.age = age
        user.hobby = hobby

        db.session.commit()
        flash('Данные успешно обновлены!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_account.html', account=account, user=user, title=pages['edit_account.html'])


# Выход
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('login'))
