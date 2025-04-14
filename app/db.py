from config import DB_PARAMS
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(**DB_PARAMS)


def create_users_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            city TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            hobby TEXT NOT NULL,
            age INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS accounts (
            user_id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


def save_user(user_data):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO users (name, city, email, hobby, age)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (email) DO NOTHING
        """, (
            user_data['name'],
            user_data['city'],
            user_data['email'],
            user_data['hobby'],
            int(user_data['age'])
        ))
        conn.commit()
    finally:
        cur.close()
        conn.close()


def load_users():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM users ORDER BY user_id DESC")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

def check_email_exists(email):
    # Подключение к базе данных
    conn = get_connection()
    cur = conn.cursor()

    # Выполнение запроса на поиск email в базе данных
    query = sql.SQL("SELECT 1 FROM users WHERE email = %s LIMIT 1")
    cur.execute(query, (email,))
    result = cur.fetchone()

    cur.close()
    conn.close()

    # Если результат не None, значит email уже существует
    return result is not None

