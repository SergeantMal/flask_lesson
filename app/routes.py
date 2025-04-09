from flask import Flask, render_template, jsonify, redirect, url_for, request
from datetime import datetime
import json
import os
from app import app


MONTHS_RU = {
    1: "января", 2: "февраля", 3: "марта", 4: "апреля",
    5: "мая", 6: "июня", 7: "июля", 8: "августа",
    9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
}

pages = {
    "index.html": "Урок <strong>VD05</strong>",
    "blog.html": "<strong>Блог</strong>",
    "contacts.html": "<strong>Контакты</strong>",
    "form.html": "<strong>Анкета пользователя</strong>"
}

DATA_FILE = 'app/data/users.json'


def load_users():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_user(user_data):
    users = load_users()
    users.append(user_data)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)



@app.route('/')
def index():
    return render_template('index.html', title=pages['index.html'])

@app.route('/blog/')
def about():
    return render_template('blog.html', title=pages['blog.html'])

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

        if user_data['name'] and user_data['email'] and user_data['city'] and user_data['hobby'] and user_data['age']:
            save_user(user_data)

        return redirect(url_for('form'))
    users = load_users()

    return render_template('form.html', title=pages['form.html'], users=users)

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