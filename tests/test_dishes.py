"""Тесты класса Dish и функций работы с блюдами."""

from models import Dish
from models.dishes import (
    add_dish,
    filter_dishes_by_category,
    filter_dishes_by_price,
    find_dish,
    sort_dishes,
)


def test_dish_creation():
    dish = Dish(1, "Капучино", "Напитки", 250.0, True, "С молоком")
    assert dish.id == 1
    assert dish.name == "Капучино"
    assert dish.category == "Напитки"
    assert dish.price == 250.0
    assert dish.in_stock is True


def test_dish_is_available():
    available = Dish(1, "Капучино", "Напитки", 250.0, in_stock=True)
    unavailable = Dish(2, "Чизкейк", "Десерты", 320.0, in_stock=False)
    assert available.is_available()
    assert not unavailable.is_available()


def test_dish_is_affordable():
    dish = Dish(1, "Капучино", "Напитки", 250.0)
    assert dish.is_affordable(300.0)
    assert not dish.is_affordable(200.0)


def test_dish_validate_price():
    assert Dish.validate_price(100)
    assert Dish.validate_price(0.5)
    assert not Dish.validate_price(0)
    assert not Dish.validate_price(-10)


def test_dish_str():
    dish = Dish(1, "Капучино", "Напитки", 250.0)
    text = str(dish)
    assert "Капучино" in text
    assert "Напитки" in text
    assert "250" in text


def test_dish_from_data():
    data = {
        "id": 1, "name": "Капучино", "category": "Напитки",
        "price": 250.0, "in_stock": True, "description": "Кофе",
    }
    dish = Dish.from_data(data)
    assert dish.id == 1
    assert dish.name == "Капучино"


def test_add_dish():
    dishes = []
    add_dish(dishes, "Капучино", "Напитки", 250.0)
    add_dish(dishes, "Цезарь", "Салаты", 450.0)
    assert len(dishes) == 2
    assert dishes[0].id == 1
    assert dishes[1].id == 2


def test_find_dish():
    dishes = []
    add_dish(dishes, "Капучино", "Напитки", 250.0)
    add_dish(dishes, "Цезарь", "Салаты", 450.0)
    add_dish(dishes, "Латте", "Напитки", 280.0)
    result = find_dish(dishes, "капу")
    assert len(result) == 1
    assert result[0].name == "Капучино"


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
    add_dish(dishes, "Чизкейк", "Десерты", 320.0)
    cheap = filter_dishes_by_price(dishes, 300.0)
    assert len(cheap) == 1
    assert cheap[0].name == "Капучино"


def test_sort_dishes_by_price():
    dishes = []
    add_dish(dishes, "Цезарь", "Салаты", 450.0)
    add_dish(dishes, "Капучино", "Напитки", 250.0)
    add_dish(dishes, "Чизкейк", "Десерты", 320.0)
    sorted_dishes = sort_dishes(dishes, by="price")
    prices = [dish.price for dish in sorted_dishes]
    assert prices == [250.0, 320.0, 450.0]
