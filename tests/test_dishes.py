"""Тесты для функций работы с блюдами."""

from dishes import (
    add_dish,
    calculate_order,
    check_availability,
    filter_dishes_by_category,
    filter_dishes_by_price,
    find_dish,
    sort_dishes,
)


def test_add_dish():
    dishes = []
    add_dish(dishes, "Капучино", "Напитки", 250.0)
    add_dish(dishes, "Цезарь", "Салаты", 450.0)

    assert len(dishes) == 2
    assert dishes[0]["id"] == 1
    assert dishes[1]["id"] == 2
    assert dishes[0]["name"] == "Капучино"


def test_find_dish():
    dishes = []
    add_dish(dishes, "Капучино", "Напитки", 250.0)
    add_dish(dishes, "Цезарь", "Салаты", 450.0)
    add_dish(dishes, "Латте", "Напитки", 280.0)

    result = find_dish(dishes, "капу")
    assert len(result) == 1
    assert result[0]["name"] == "Капучино"


def test_filter_dishes_by_category():
    dishes = []
    add_dish(dishes, "Капучино", "Напитки", 250.0)
    add_dish(dishes, "Цезарь", "Салаты", 450.0)
    add_dish(dishes, "Латте", "Напитки", 280.0)

    drinks = filter_dishes_by_category(dishes, "Напитки")
    assert len(drinks) == 2


def test_filter_dishes_by_price():
    dishes = []
    add_dish(dishes, "Капучино", "Напитки", 250.0)
    add_dish(dishes, "Цезарь", "Салаты", 450.0)
    add_dish(dishes, "Чизкейк", "Десерты", 280.0)

    cheap = filter_dishes_by_price(dishes, 300.0)
    assert len(cheap) == 2
    assert all(dish["price"] <= 300.0 for dish in cheap)


def test_sort_dishes_by_price():
    dishes = []
    add_dish(dishes, "Цезарь", "Салаты", 450.0)
    add_dish(dishes, "Капучино", "Напитки", 250.0)
    add_dish(dishes, "Чизкейк", "Десерты", 320.0)

    sorted_dishes = sort_dishes(dishes, by="price")
    prices = [dish["price"] for dish in sorted_dishes]
    assert prices == [250.0, 320.0, 450.0]


def test_check_availability():
    available = {"id": 1, "name": "Капучино", "in_stock": True}
    unavailable = {"id": 2, "name": "Цезарь", "in_stock": False}

    assert check_availability(available) == "Блюдо в наличии"
    assert check_availability(unavailable) == "Блюдо временно недоступно"


def test_calculate_order():
    dish = {"id": 1, "name": "Капучино", "price": 250.0}

    assert calculate_order(dish, quantity=1) == 250.0
    assert calculate_order(dish, quantity=2, discount_percent=10.0) == 450.0
    assert calculate_order(dish, quantity=3, discount_percent=0.0) == 750.0