"""Класс Dish и функции работы с коллекцией блюд."""

from typing import Optional


class Dish:
    """Блюдо из меню заведения.

    Атрибуты:
        id: уникальный идентификатор блюда;
        name: название блюда;
        category: название категории;
        price: цена в рублях;
        in_stock: есть ли блюдо в наличии;
        description: краткое описание.
    """

    def __init__(
        self,
        dish_id: int,
        name: str,
        category: str,
        price: float,
        in_stock: bool = True,
        description: str = "",
    ) -> None:
        """Создать объект блюда."""
        self.id = dish_id
        self.name = name
        self.category = category
        self.price = price
        self.in_stock = in_stock
        self.description = description

    def is_available(self) -> bool:
        """Проверить, доступно ли блюдо к заказу."""
        return self.in_stock

    def is_affordable(self, max_price: float) -> bool:
        """Проверить, что цена блюда не превышает max_price."""
        return self.price <= max_price

    def __str__(self) -> str:
        """Вернуть строковое представление блюда."""
        status = "в наличии" if self.in_stock else "нет в наличии"
        return (
            f"{self.name} ({self.category}) — {self.price} руб. "
            f"[{status}] — {self.description}"
        )

    @classmethod
    def from_data(cls, data: dict) -> "Dish":
        """Создать блюдо из словаря (например, из JSON)."""
        return cls(
            dish_id=data["id"],
            name=data["name"],
            category=data["category"],
            price=data["price"],
            in_stock=data.get("in_stock", True),
            description=data.get("description", ""),
        )

    def to_data(self) -> dict:
        """Преобразовать блюдо в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "in_stock": self.in_stock,
            "description": self.description,
        }

    @staticmethod
    def validate_price(price: float) -> bool:
        """Проверить, что цена корректна (положительное число)."""
        return isinstance(price, (int, float)) and price > 0


def add_dish(
    dishes: list[Dish],
    name: str,
    category: str,
    price: float,
    in_stock: bool = True,
    description: str = "",
) -> Dish:
    """Создать новый объект Dish и добавить его в коллекцию."""
    if dishes:
        new_id = max(dish.id for dish in dishes) + 1
    else:
        new_id = 1

    dish = Dish(new_id, name, category, price, in_stock, description)
    dishes.append(dish)
    return dish


def find_dish(dishes: list[Dish], query: str) -> list[Dish]:
    """Найти блюда, в названии которых встречается подстрока query."""
    query_lower = query.lower()
    return [dish for dish in dishes if query_lower in dish.name.lower()]


def find_dish_by_id(dishes: list[Dish], dish_id: int) -> Optional[Dish]:
    """Найти блюдо по идентификатору. Вернуть None, если не найдено."""
    for dish in dishes:
        if dish.id == dish_id:
            return dish
    return None


def filter_dishes_by_category(
    dishes: list[Dish], category: str
) -> list[Dish]:
    """Отобрать блюда указанной категории."""
    return [dish for dish in dishes if dish.category == category]


def filter_dishes_by_price(
    dishes: list[Dish], max_price: float
) -> list[Dish]:
    """Отобрать блюда, цена которых не превышает max_price."""
    return [dish for dish in dishes if dish.is_affordable(max_price)]


def sort_dishes(
    dishes: list[Dish], by: str = "price", reverse: bool = False
) -> list[Dish]:
    """Отсортировать блюда по указанному атрибуту."""
    return sorted(dishes, key=lambda dish: getattr(dish, by), reverse=reverse)


def show_dishes(dishes: list[Dish]) -> None:
    """Напечатать список блюд."""
    if not dishes:
        print("Список блюд пуст.")
        return
    for dish in dishes:
        print(" -", dish)
