import logging
import sqlite3

logger = logging.getLogger(__name__)

DB = "arayadak.db"


def connect():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    try:
        with connect() as conn:
            conn.execute("""
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
        logger.info("Database tables ready.")
    except sqlite3.Error as e:
        logger.error("Error creating tables: %s", e)
        raise


def add_order(user_id, name, phone, product):
    try:
        with connect() as conn:
            conn.execute(
                """
                INSERT INTO orders (user_id, name, phone, product, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, name, phone, product, "در حال بررسی"),
            )
            conn.commit()
    except sqlite3.Error as e:
        logger.error("Error adding order: %s", e)
        raise
