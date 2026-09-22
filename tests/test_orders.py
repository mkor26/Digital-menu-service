"""Тесты класса Order и функций работы с заказами."""

from models import Dish, Order, User
from models.orders import (
    add_order,
    cancel_order,
    filter_orders_by_user,
    find_order_by_id,
)


def _make_dish():
    return Dish(1, "Капучино", "Напитки", 250.0)


def _make_user():
    return User(1, "Иван Петров", "ivan@example.com")


def test_order_creation():
    dish = _make_dish()
    user = _make_user()
    order = Order(1, dish, user, quantity=2, discount_percent=10.0)

    assert order.id == 1
    assert order.dish is dish
    assert order.user is user
    assert order.quantity == 2
    assert order.is_cancelled is False


def test_order_total():
    dish = _make_dish()
    user = _make_user()
    order = Order(1, dish, user, quantity=2, discount_percent=10.0)
    assert order.total() == 450.0


def test_order_total_no_discount():
    dish = _make_dish()
    user = _make_user()
    order = Order(1, dish, user, quantity=3)
    assert order.total() == 750.0


def test_order_cancel():
    dish = _make_dish()
    user = _make_user()
    order = Order(1, dish, user)
    order.cancel()
    assert order.is_cancelled


def test_order_str():
    dish = _make_dish()
    user = _make_user()
    order = Order(1, dish, user, quantity=2)
    text = str(order)
    assert "Капучино" in text
    assert "Иван Петров" in text


def test_add_order():
    dish = _make_dish()
    user = _make_user()
    orders = []
    add_order(orders, dish, user)
    add_order(orders, dish, user, quantity=2)
    assert len(orders) == 2
    assert orders[0].id == 1
    assert orders[1].id == 2


def test_find_order_by_id():
    dish = _make_dish()
    user = _make_user()
    orders = []
    order = add_order(orders, dish, user)
    assert find_order_by_id(orders, order.id) is order
    assert find_order_by_id(orders, 99) is None


def test_cancel_order():
    dish = _make_dish()
    user = _make_user()
    orders = []
    order = add_order(orders, dish, user)
    assert cancel_order(orders, order.id)
    assert order.is_cancelled
    assert not cancel_order(orders, 999)


def test_filter_orders_by_user():
    dish = _make_dish()
    user1 = User(1, "Иван", "ivan@example.com")
    user2 = User(2, "Мария", "maria@example.com")
    orders = []
    add_order(orders, dish, user1)
    add_order(orders, dish, user2)
    add_order(orders, dish, user1)

    active_ivan = filter_orders_by_user(orders, user1)
    assert len(active_ivan) == 2
