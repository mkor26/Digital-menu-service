"""Подключение к SQLite и функции получения данных для Django."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "digital_menu.sqlite"


@contextmanager
def get_connection():
    """Открыть соединение с SQLite и гарантированно закрыть его."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def fetch_all(query, params=()):
    """Выполнить SELECT и вернуть строки результата."""
    with get_connection() as connection:
        return connection.execute(query, params).fetchall()


def fetch_one(query, params=()):
    """Выполнить SELECT и вернуть одну строку либо None."""
    with get_connection() as connection:
        return connection.execute(query, params).fetchone()


def get_categories():
    return fetch_all("SELECT id, name FROM categories ORDER BY name")


def get_dishes(category_id=None, max_price=None, available_only=False):
    """Получить блюда с категорией; фильтры передаются параметрами SQL."""
    query = """SELECT d.id, d.name, c.name AS category, d.price,
                      d.in_stock, d.description
               FROM dishes AS d
               JOIN categories AS c ON c.id = d.category_id
               WHERE 1 = 1"""
    params = []
    if category_id:
        query += " AND d.category_id = ?"
        params.append(category_id)
    if max_price is not None:
        query += " AND d.price <= ?"
        params.append(max_price)
    if available_only:
        query += " AND d.in_stock = 1"
    query += " ORDER BY d.name"
    return fetch_all(query, params)


def get_dish(dish_id):
    return fetch_one(
        """SELECT d.id, d.name, c.name AS category, d.price,
                  d.in_stock, d.description
           FROM dishes AS d JOIN categories AS c ON c.id = d.category_id
           WHERE d.id = ?""",
        (dish_id,),
    )


def get_orders():
    return fetch_all(
        """SELECT o.id, d.name AS dish_name, u.name AS user_name,
                  o.quantity, o.discount_percent, o.is_cancelled,
                  ROUND(d.price * o.quantity *
                        (1 - o.discount_percent / 100.0), 2) AS total
           FROM orders AS o
           JOIN dishes AS d ON d.id = o.dish_id
           JOIN users AS u ON u.id = o.user_id
           ORDER BY o.id"""
    )


def get_order(order_id):
    return fetch_one(
        """SELECT o.id, d.name AS dish_name, u.name AS user_name,
                  u.email AS user_email, o.quantity, o.discount_percent,
                  o.is_cancelled,
                  ROUND(d.price * o.quantity *
                        (1 - o.discount_percent / 100.0), 2) AS total
           FROM orders AS o
           JOIN dishes AS d ON d.id = o.dish_id
           JOIN users AS u ON u.id = o.user_id
           WHERE o.id = ?""",
        (order_id,),
    )


def get_statistics():
    summary = fetch_one(
        """SELECT COUNT(*) AS dishes_count,
                  SUM(CASE WHEN in_stock = 1 THEN 1 ELSE 0 END)
                      AS available_count,
                  MIN(price) AS min_price, MAX(price) AS max_price,
                  ROUND(AVG(price), 2) AS average_price
           FROM dishes"""
    )
    categories = fetch_all(
        """SELECT c.name AS category, COUNT(d.id) AS dishes_count
           FROM categories AS c
           LEFT JOIN dishes AS d ON d.category_id = c.id
           GROUP BY c.id, c.name ORDER BY c.name"""
    )
    orders_count = fetch_one(
        """SELECT COUNT(*) AS orders_count,
                  SUM(CASE WHEN is_cancelled = 0 THEN 1 ELSE 0 END)
                      AS active_orders
           FROM orders"""
    )
    return summary, categories, orders_count
