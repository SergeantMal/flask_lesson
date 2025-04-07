from flask import Flask, render_template, jsonify
from datetime import datetime


MONTHS_RU = {
    1: "января", 2: "февраля", 3: "марта", 4: "апреля",
    5: "мая", 6: "июня", 7: "июля", 8: "августа",
    9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
}

pages = {
    "index.html": "Урок <strong>VD05</strong>",
    "blog.html": "<strong>Блог</strong>",
    "contacts.html": "<strong>Контакты</strong>"
}
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
