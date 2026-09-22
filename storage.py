"""Сохранение и загрузка данных проекта в JSON.

Загрузка: JSON → объекты классов.
Сохранение: объекты классов → JSON.
"""

import json
import os

from models import Category, Dish, Order, User
from models.dishes import find_dish_by_id
from models.users import find_user_by_id


def _ensure_dir(filename: str) -> None:
    """Создать папку для файла, если её нет."""
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)


def _load_json(filename: str) -> list[dict]:
    """Загрузить JSON-файл как список словарей."""
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден, будет создан новый.")
        return []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        print(f"Не удалось прочитать {filename}: {error}")
        return []


def _save_json(filename: str, data: list[dict]) -> None:
    """Сохранить список словарей в JSON."""
    _ensure_dir(filename)
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except OSError as error:
        print(f"Не удалось сохранить {filename}: {error}")


# === Блюда ===

def load_dishes(filename: str) -> list[Dish]:
    """Загрузить блюда из JSON и превратить их в объекты Dish."""
    data = _load_json(filename)
    return [Dish.from_data(item) for item in data]


def save_dishes(filename: str, dishes: list[Dish]) -> None:
    """Сохранить объекты Dish в JSON."""
    _save_json(filename, [dish.to_data() for dish in dishes])


# === Категории ===

def load_categories(filename: str) -> list[Category]:
    """Загрузить категории из JSON и превратить их в объекты Category."""
    data = _load_json(filename)
    return [Category.from_data(item) for item in data]


def save_categories(filename: str, categories: list[Category]) -> None:
    """Сохранить объекты Category в JSON."""
    _save_json(filename, [c.to_data() for c in categories])


# === Пользователи ===

def load_users(filename: str) -> list[User]:
    """Загрузить пользователей из JSON и превратить их в объекты User."""
    data = _load_json(filename)
    return [User.from_data(item) for item in data]


def save_users(filename: str, users: list[User]) -> None:
    """Сохранить объекты User в JSON."""
    _save_json(filename, [user.to_data() for user in users])


# === Заказы ===

def load_orders(
    filename: str, dishes: list[Dish], users: list[User]
) -> list[Order]:
    """Загрузить заказы из JSON, восстановив связи с Dish и User.

    В JSON хранятся только идентификаторы dish_id и user_id —
    при загрузке они превращаются в ссылки на объекты.
    """
    data = _load_json(filename)
    orders: list[Order] = []

    for item in data:
        dish = find_dish_by_id(dishes, item["dish_id"])
        user = find_user_by_id(users, item["user_id"])
        if dish is None or user is None:
            print(
                f"Пропущен заказ №{item['id']}: "
                f"не найдено блюдо или пользователь."
            )
            continue

        order = Order(
            order_id=item["id"],
            dish=dish,
            user=user,
            quantity=item["quantity"],
            discount_percent=item.get("discount_percent", 0.0),
        )
        order.is_cancelled = item.get("is_cancelled", False)
        orders.append(order)

    return orders


def save_orders(filename: str, orders: list[Order]) -> None:
    """Сохранить заказы в JSON (только идентификаторы связанных объектов)."""
    data = [
        {
            "id": order.id,
            "dish_id": order.dish.id,
            "user_id": order.user.id,
            "quantity": order.quantity,
            "discount_percent": order.discount_percent,
            "is_cancelled": order.is_cancelled,
        }
        for order in orders
    ]
    _save_json(filename, data)
