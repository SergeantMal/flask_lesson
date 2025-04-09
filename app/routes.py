from flask import render_template, jsonify, redirect, url_for, request, flash
from datetime import datetime
from app.db import save_user, load_users, check_email_exists
from app import app


MONTHS_RU = {
    1: "января", 2: "февраля", 3: "марта", 4: "апреля",
    5: "мая", 6: "июня", 7: "июля", 8: "августа",
    9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
}

pages = {
    "index.html": "Урок <strong>VD06</strong>",
    "blog.html": "<strong>Блог</strong>",
    "contacts.html": "<strong>Контакты</strong>",
    "form.html": "<strong>Анкета пользователя</strong>"
}




@app.route('/')
def index():
    return render_template('index.html', title=pages['index.html'])

@app.route('/blog/')
def about():
    return render_template('blog.html', title=pages['blog.html'])

from flask import flash, redirect, url_for, render_template, request

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
            # Проверяем, существует ли email в базе данных
            if check_email_exists(user_data['email']):
                flash('Этот email уже зарегистрирован. Пожалуйста, используйте другой email.', 'error')
                return render_template('form.html', title=pages['form.html'], user_data=user_data)

            else:
                # Если email не существует, сохраняем пользователя
                save_user(user_data)
                flash('Пользователь успешно добавлен!', 'success')
                return redirect(url_for('form'))  # Перенаправляем на форму и очищаем поля

    # Загружаем пользователей для отображения на странице
    users = load_users()

    # Передаем пустые данные или введенные ранее данные
    user_data = {
        'name': '',
        'email': '',
        'city': '',
        'hobby': '',
        'age': ''
    }

    return render_template('form.html', title=pages['form.html'], users=users, user_data=user_data)


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