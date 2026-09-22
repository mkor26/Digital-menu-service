"""Класс Order и функции работы с коллекцией заказов.

Заказ связывает блюдо (Dish) и пользователя (User).
"""

from typing import Optional

from .dishes import Dish
from .users import User


class Order:
    """Заказ блюда пользователем.

    Атрибуты:
        id: идентификатор заказа;
        dish: объект Dish, который заказали;
        user: объект User, который заказал;
        quantity: количество порций;
        discount_percent: скидка в процентах;
        is_cancelled: признак отмены заказа.
    """

    def __init__(
        self,
        order_id: int,
        dish: Dish,
        user: User,
        quantity: int = 1,
        discount_percent: float = 0.0,
    ) -> None:
        """Создать объект заказа."""
        self.id = order_id
        self.dish = dish
        self.user = user
        self.quantity = quantity
        self.discount_percent = discount_percent
        self.is_cancelled = False

    def total(self) -> float:
        """Посчитать итоговую стоимость заказа с учётом скидки."""
        gross = self.dish.price * self.quantity
        discount = gross * self.discount_percent / 100
        return gross - discount

    def cancel(self) -> None:
        """Отменить заказ."""
        self.is_cancelled = True

    def status(self) -> str:
        """Вернуть текстовый статус заказа."""
        return "отменён" if self.is_cancelled else "активен"

    def __str__(self) -> str:
        """Вернуть строковое представление заказа."""
        return (
            f"Заказ №{self.id}: {self.quantity} × {self.dish.name} "
            f"для {self.user.name} — {self.total():.2f} руб. "
            f"[{self.status()}]"
        )


def add_order(
    orders: list[Order],
    dish: Dish,
    user: User,
    quantity: int = 1,
    discount_percent: float = 0.0,
) -> Order:
    """Создать заказ и добавить его в коллекцию."""
    if orders:
        new_id = max(order.id for order in orders) + 1
    else:
        new_id = 1

    order = Order(new_id, dish, user, quantity, discount_percent)
    orders.append(order)
    return order


def find_order_by_id(orders: list[Order], order_id: int) -> Optional[Order]:
    """Найти заказ по идентификатору."""
    for order in orders:
        if order.id == order_id:
            return order
    return None


def cancel_order(orders: list[Order], order_id: int) -> bool:
    """Отменить заказ по идентификатору.

    Возвращает True, если заказ найден и отменён, иначе False.
    """
    order = find_order_by_id(orders, order_id)
    if order is None:
        return False
    order.cancel()
    return True


def filter_orders_by_user(
    orders: list[Order], user: User
) -> list[Order]:
    """Вернуть активные заказы указанного пользователя."""
    return [
        order
        for order in orders
        if order.user is user and not order.is_cancelled
    ]


def show_orders(orders: list[Order]) -> None:
    """Напечатать заказы."""
    if not orders:
        print("Список заказов пуст.")
        return
    for order in orders:
        print(" -", order)
