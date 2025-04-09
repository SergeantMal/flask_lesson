
# Flask Lesson

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3-lightgrey.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supported-blue)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Простое учебное веб-приложение на Flask с подключением к PostgreSQL.

## 📦 Описание

Проект демонстрирует базовую структуру Flask-приложения с разделением на модули, использованием шаблонов и подключением к базе данных PostgreSQL. В качестве хранилища используется таблица пользователей, создаваемая при старте приложения.

## 🚀 Установка и запуск

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/SergeantMal/flask_lesson.git
cd flask_lesson
```

### 2. Создайте и активируйте виртуальное окружение

```bash
python -m venv venv
# Для Windows:
venv\Scripts\activate
# Для Unix/MacOS:
source venv/bin/activate
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Создайте файл `config.py` в корневой директории

```python
DB_PARAMS = {
    "dbname": "имя_БД",
    "user": "имя_пользователя",
    "password": "пароль",
    "host": "IP_БД",
    "port": "порт_БД",
    "client_encoding": "UTF8"
}
```

### 5. Запустите приложение

```bash
python main.py
```

👉 `http://127.0.0.1:5000/`

## 📁 Структура проекта

```
flask_lesson/
│
├── app/
│   ├── __init__.py
│   ├── db.py
│   ├── routes.py
│   ├── static/
│   └── templates/
│
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

## 📜 Лицензия

Этот проект распространяется под лицензией MIT.

## 🧑‍💻 Автор

[SergeantMal](https://github.com/SergeantMal)

---

# Flask Lesson (English)

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3-lightgrey.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supported-blue)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple educational web app built with Flask and PostgreSQL.

## 📦 Description

This project demonstrates a basic Flask application structure with routing, templates, and PostgreSQL database integration. A user table is automatically created on startup.

## 🚀 Installation & Running

### 1. Clone the repository

```bash
git clone https://github.com/SergeantMal/flask_lesson.git
cd flask_lesson
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Unix/MacOS:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `config.py` in the root directory

```python
DB_PARAMS = {
    "dbname": "your_db_name",
    "user": "your_username",
    "password": "your_password",
    "host": "db_ip",
    "port": "db_port",
    "client_encoding": "UTF8"
}
```

### 5. Run the app

```bash
python main.py
```

Visit 👉 `http://127.0.0.1:5000/`

## 📁 Project structure

```
flask_lesson/
├── app/
│   ├── __init__.py
│   ├── db.py
│   ├── routes.py
│   ├── static/
│   └── templates/
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

## 📜 License

Licensed under the MIT License.

## 🧑‍💻 Author

[SergeantMal](https://github.com/SergeantMal)
