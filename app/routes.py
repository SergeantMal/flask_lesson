from flask import render_template, jsonify, redirect, url_for, request, flash, Blueprint, current_app
from datetime import datetime
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from deep_translator import GoogleTranslator

from app.database import save_user, load_users, check_email_exists
from app.models import db, User, Accounts
from app.forms import RegisterForm, LoginForm


routes = Blueprint('routes', __name__)

MONTHS_RU = {
    1: "января", 2: "февраля", 3: "марта", 4: "апреля",
    5: "мая", 6: "июня", 7: "июля", 8: "августа",
    9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
}

pages = {
    "index.html": "Урок <strong>VD08</strong>",
    "blog.html": "<strong>Блог</strong>",
    "contacts.html": "<strong>Контакты</strong>",
    "form.html": "<strong>Анкета пользователя</strong>",
    "account.html": "<strong>Личный кабинет</strong>",
    "register.html": "<strong>Регистрация</strong>",
    "login.html": "<strong>Вход</strong>",
    "edit_account.html": "<strong>Редактирование профиля</strong>"
}



IPINFO_TOKEN = '83796ee2e81f45'

@routes.route('/detect-location')
def detect_location():
    client_ip = request.remote_addr  # Получаем IP-адрес клиента

    try:
        response = requests.get(f'https://ipinfo.io/{client_ip}/json?token={IPINFO_TOKEN}')
        data = response.json()
        city = data.get('city', 'Default City')
        return jsonify({'city': city})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'city': 'Default City'})



@routes.route('/api/weather/<city>')
def get_weather(city):
    API_KEY = 'fc4a628ded5e41efac0174832251904'  # Хранится только на сервере
    url = f'https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&lang=ru'

    try:
        response = requests.get(url)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


@routes.route('/', methods=['GET', 'POST'])
def index():
    translation = None

    quote = {
        "text": "",
        "author": ""
    }

    # Загружаем новую цитату (GET)
    if request.method == 'GET':
        try:
            response = requests.get("https://zenquotes.io/api/random")
            data = response.json()[0]  # Это массив с одним словарём
            quote['text'] = data['q']
            quote['author'] = data['a']
        except Exception as e:
            quote['text'] = f"Ошибка загрузки цитаты: {e}"

    # Переводим цитату (POST)
    if request.method == 'POST':
        quote['text'] = request.form.get('text')
        quote['author'] = request.form.get('author')
        try:
            translation = GoogleTranslator(source='auto', target='ru').translate(quote['text'])
        except Exception as e:
            translation = "Ошибка перевода."

    return render_template('index.html', quote=quote, translation=translation, title=pages['index.html'])


@routes.route('/blog/')
def about():
    return render_template('blog.html', title=pages['blog.html'])

@routes.route('/contacts/')
def contact():
    return render_template('contacts.html', title=pages['contacts.html'])

@routes.route('/time')
def get_time():
    now = datetime.now()
    formatted_date = f"{now.day} {MONTHS_RU[now.month]} {now.year}"
    return jsonify({
        "time": now.strftime("%H:%M:%S"),
        "date": formatted_date
    })


@routes.route('/form/', methods=["GET", "POST"])
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


@routes.route('/register', methods=['GET', 'POST'])
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
            return redirect(url_for('routes.login'))

    return render_template('register.html', form=form, title=pages['register.html'])


# Авторизация
@routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Accounts.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Вы вошли в систему!', 'success')
            return redirect(url_for('routes.dashboard'))
        else:
            flash('Неверный логин или пароль', 'danger')
    return render_template('login.html', form=form, title=pages['login.html'])

# Личный кабинет (доступен только авторизованным)
@routes.route('/account')
@login_required
def dashboard():
    login_manager = current_app.login_manager
    account = Accounts.query.get(current_user.user_id)
    user = User.query.filter_by(email=account.email).first()
    return render_template('account.html', account=account, user=user, title=pages['account.html'])


@routes.route('/account/edit', methods=['GET', 'POST'])
@login_required
def edit_account():
    login_manager = current_app.login_manager
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
            return redirect(url_for('routes.edit_account'))

        account.email = new_email
        if new_password:
            account.password = generate_password_hash(new_password)

        if user is None:
            # Создаём нового пользователя
            user = User(
                email=new_email,
                name=new_name,
                city=city,
                age=age,
                hobby=hobby
            )
            db.session.add(user)
        else:
            # Обновляем данные
            user.name = new_name
            user.email = new_email
            user.city = city
            user.age = age
            user.hobby = hobby

        db.session.commit()
        flash('Данные успешно обновлены!', 'success')
        return redirect(url_for('routes.dashboard'))

    return render_template('edit_account.html', account=account, user=user, title=pages['edit_account.html'])

# Выход
@routes.route('/logout')
@login_required
def logout():
    login_manager = current_app.login_manager
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('routes.login'))
