"""Однократный перенос исходных JSON-данных в SQLite."""

import json
from pathlib import Path

from db.database import DB_PATH, get_connection

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def read_json(filename):
    with (DATA_DIR / filename).open("r", encoding="utf-8") as file:
        return json.load(file)


def import_data():
    categories = read_json("categories.json")
    dishes = read_json("dishes.json")
    users = read_json("users.json")
    orders = read_json("orders.json")

    with get_connection() as connection:
        schema_path = BASE_DIR / "sql" / "schema.sql"
        connection.executescript(schema_path.read_text(encoding="utf-8"))
        cursor = connection.cursor()
        cursor.execute("DELETE FROM orders")
        cursor.execute("DELETE FROM dishes")
        cursor.execute("DELETE FROM users")
        cursor.execute("DELETE FROM categories")

        cursor.executemany(
            "INSERT INTO categories (id, name) VALUES (?, ?)",
            [(item["id"], item["name"]) for item in categories],
        )

        # В исходном categories.json присутствуют не все категории блюд.
        # Добавляем недостающие названия, не меняя исходные JSON-файлы.
        known_names = {item["name"] for item in categories}
        missing_names = sorted(
            {item["category"] for item in dishes} - known_names
        )
        cursor.executemany(
            "INSERT INTO categories (name) VALUES (?)",
            [(name,) for name in missing_names],
        )

        category_ids = {
            row["name"]: row["id"]
            for row in cursor.execute("SELECT id, name FROM categories")
        }
        cursor.executemany(
            """INSERT INTO dishes
               (id, name, category_id, price, in_stock, description)
               VALUES (?, ?, ?, ?, ?, ?)""",
            [
                (
                    item["id"], item["name"], category_ids[item["category"]],
                    item["price"], int(item.get("in_stock", True)),
                    item.get("description", ""),
                )
                for item in dishes
            ],
        )
        cursor.executemany(
            "INSERT INTO users (id, name, email) VALUES (?, ?, ?)",
            [(item["id"], item["name"], item["email"]) for item in users],
        )
        cursor.executemany(
            """INSERT INTO orders
               (id, dish_id, user_id, quantity, discount_percent, is_cancelled)
               VALUES (?, ?, ?, ?, ?, ?)""",
            [
                (
                    item["id"], item["dish_id"], item["user_id"],
                    item["quantity"], item.get("discount_percent", 0),
                    int(item.get("is_cancelled", False)),
                )
                for item in orders
            ],
        )

    print(f"Импорт завершён: {DB_PATH}")
    print(
        f"Категорий: {len(category_ids)}, блюд: {len(dishes)}, "
        f"пользователей: {len(users)}, заказов: {len(orders)}"
    )


if __name__ == "__main__":
    import_data()
