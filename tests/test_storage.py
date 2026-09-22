"""Тесты сохранения и загрузки объектов в JSON."""

import os

from models import Category, Dish, Order, User
from storage import (
    load_categories,
    load_dishes,
    load_orders,
    load_users,
    save_categories,
    save_dishes,
    save_orders,
    save_users,
)


def test_save_and_load_dishes(tmp_path):
    filename = os.path.join(tmp_path, "dishes.json")
    dishes = [Dish(1, "Капучино", "Напитки", 250.0)]
    save_dishes(filename, dishes)
    loaded = load_dishes(filename)
    assert len(loaded) == 1
    assert loaded[0].name == "Капучино"
    assert loaded[0].price == 250.0


def test_save_and_load_categories(tmp_path):
    filename = os.path.join(tmp_path, "categories.json")
    categories = [Category(1, "Напитки")]
    save_categories(filename, categories)
    loaded = load_categories(filename)
    assert len(loaded) == 1
    assert loaded[0].name == "Напитки"


def test_save_and_load_users(tmp_path):
    filename = os.path.join(tmp_path, "users.json")
    users = [User(1, "Иван", "ivan@example.com")]
    save_users(filename, users)
    loaded = load_users(filename)
    assert len(loaded) == 1
    assert loaded[0].email == "ivan@example.com"


def test_save_and_load_orders(tmp_path):
    """Проверить, что ссылки на Dish и User восстанавливаются."""
    filename = os.path.join(tmp_path, "orders.json")
    dish = Dish(1, "Капучино", "Напитки", 250.0)
    user = User(1, "Иван", "ivan@example.com")
    order = Order(1, dish, user, quantity=2, discount_percent=10.0)

    save_orders(filename, [order])
    loaded = load_orders(filename, [dish], [user])

    assert len(loaded) == 1
    assert loaded[0].dish is dish
    assert loaded[0].user is user
    assert loaded[0].quantity == 2
    assert loaded[0].discount_percent == 10.0


def test_load_missing_file(tmp_path, capsys):
    filename = os.path.join(tmp_path, "missing.json")
    result = load_dishes(filename)
    assert result == []
    captured = capsys.readouterr()
    assert "не найден" in captured.out


def test_load_broken_json(tmp_path, capsys):
    filename = os.path.join(tmp_path, "broken.json")
    with open(filename, "w", encoding="utf-8") as file:
        file.write("{это не JSON}")

    result = load_dishes(filename)
    assert result == []
    captured = capsys.readouterr()
    assert "Не удалось прочитать" in captured.out
