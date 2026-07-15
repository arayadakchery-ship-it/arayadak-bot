import sqlite3

DB = "arayadak.db"


def connect():
    return sqlite3.connect(DB)


def create_tables():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        phone TEXT,
        product TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_order(user_id, name, phone, product):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO orders
    (user_id,name,phone,product,status)
    VALUES (?,?,?,?,?)
    """,
    (user_id,name,phone,product,"در حال بررسی"))

    conn.commit()
    conn.close()
