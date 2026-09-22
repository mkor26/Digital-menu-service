"""Модуль для работы с блюдами: добавление, поиск, фильтрация, сортировка."""

from typing import Optional


def add_dish(
    dishes: list[dict],
    name: str,
    category: str,
    price: float,
    in_stock: bool = True,
    description: str = "",
) -> dict:
    """Добавить новое блюдо в список dishes и вернуть его словарь.

    Идентификатор блюда формируется автоматически: на единицу больше
    максимального существующего id (или 1, если список пуст).
    """
    if dishes:
        new_id = max(dish["id"] for dish in dishes) + 1
    else:
        new_id = 1

    dish = {
        "id": new_id,
        "name": name,
        "category": category,
        "price": price,
        "in_stock": in_stock,
        "description": description,
    }
    dishes.append(dish)
    return dish


def find_dish(dishes: list[dict], query: str) -> list[dict]:
    """Найти блюда, в названии которых встречается подстрока query.

    Поиск выполняется без учёта регистра.
    """
    query_lower = query.lower()
    return [dish for dish in dishes if query_lower in dish["name"].lower()]


def filter_dishes_by_category(dishes: list[dict], category: str) -> list[dict]:
    """Отобрать блюда указанной категории."""
    return [dish for dish in dishes if dish["category"] == category]


def filter_dishes_by_price(
    dishes: list[dict], max_price: float
) -> list[dict]:
    """Отобрать блюда, цена которых не превышает max_price."""
    return [dish for dish in dishes if dish["price"] <= max_price]


def sort_dishes(
    dishes: list[dict], by: str = "price", reverse: bool = False
) -> list[dict]:
    """Отсортировать блюда по указанному полю (по умолчанию — по цене).

    Использует lambda-функцию в качестве ключа сортировки.
    """
    return sorted(dishes, key=lambda dish: dish.get(by, 0), reverse=reverse)


def show_dish(dish: dict) -> str:
    """Вернуть текстовое описание блюда."""
    return (
        f"{dish['name']} ({dish['category']}) — "
        f"{dish['price']} руб. — {dish['description']}"
    )


def check_availability(dish: dict) -> str:
    """Вернуть текстовый статус наличия блюда."""
    if dish["in_stock"]:
        return "Блюдо в наличии"
    return "Блюдо временно недоступно"


def calculate_order(
    dish: dict, quantity: int, discount_percent: float = 0.0
) -> float:
    """Посчитать итоговую стоимость заказа с учётом скидки."""
    total = dish["price"] * quantity
    discount = total * discount_percent / 100
    return total - discount