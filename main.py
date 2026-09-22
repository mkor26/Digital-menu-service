"""Точка запуска приложения «Digital Menu Service».

Демонстрационный сценарий работы с объектной моделью:
блюда, категории, пользователи, заказы.
"""

from models import Dish
from models.categories import add_category, show_categories
from models.dishes import (
    add_dish,
    filter_dishes_by_category,
    filter_dishes_by_price,
    find_dish,
    show_dishes,
    sort_dishes,
)
from models.orders import (
    add_order,
    cancel_order,
    filter_orders_by_user,
    show_orders,
)
from models.users import add_user, find_user, show_users
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


DISHES_FILE = "data/dishes.json"
CATEGORIES_FILE = "data/categories.json"
USERS_FILE = "data/users.json"
ORDERS_FILE = "data/orders.json"


def _seed_data(
    dishes: list[Dish],
    categories: list,
    users: list,
) -> None:
    """Заполнить пустые коллекции стартовыми данными."""
    if not dishes:
        add_dish(
            dishes, "Капучино", "Напитки", 250.0,
            description="Кофейный напиток с молочной пеной",
        )
        add_dish(
            dishes, "Цезарь", "Салаты", 450.0,
            description="Салат с курицей и пармезаном",
        )
        add_dish(
            dishes, "Чизкейк", "Десерты", 320.0,
            in_stock=False, description="Классический чизкейк",
        )

    if not categories:
        add_category(categories, "Напитки")
        add_category(categories, "Салаты")
        add_category(categories, "Десерты")

    if not users:
        add_user(users, "Иван Петров", "ivan@example.com")
        add_user(users, "Мария Сидорова", "maria@example.com")


def main() -> None:
    """Демонстрационный сценарий работы с объектами проекта."""
    print("=== Digital Menu Service ===")

    # Загрузка данных
    dishes = load_dishes(DISHES_FILE)
    categories = load_categories(CATEGORIES_FILE)
    users = load_users(USERS_FILE)
    _seed_data(dishes, categories, users)
    orders = load_orders(ORDERS_FILE, dishes, users)

    # Демонстрация блюд
    print("\n--- Все блюда ---")
    show_dishes(dishes)

    print("\n--- Поиск по подстроке 'чиз' ---")
    show_dishes(find_dish(dishes, "чиз"))

    print("\n--- Блюда категории «Напитки» ---")
    show_dishes(filter_dishes_by_category(dishes, "Напитки"))

    print("\n--- Блюда дешевле 400 руб. ---")
    show_dishes(filter_dishes_by_price(dishes, 400.0))

    print("\n--- Блюда, отсортированные по цене ---")
    show_dishes(sort_dishes(dishes, by="price"))

    print("\n--- Категории меню ---")
    show_categories(categories)

    print("\n--- Пользователи ---")
    show_users(users)

    # Демонстрация работы с объектами и заказами
    print("\n--- Оформление заказа ---")
    dish = dishes[0]
    user = users[0]
    order = add_order(orders, dish, user, quantity=2, discount_percent=10.0)
    print("Создан:", order)
    print("Проверка через атрибуты:")
    print(f"  order.dish.name  = {order.dish.name}")
    print(f"  order.user.email = {order.user.email}")
    print(f"  order.total()    = {order.total():.2f}")

    print("\n--- Поиск пользователя по подстроке 'мар' ---")
    show_users(find_user(users, "мар"))

    print("\n--- Активные заказы пользователя ---")
    show_orders(filter_orders_by_user(orders, user))

    print("\n--- Отмена заказа ---")
    cancel_order(orders, order.id)
    show_orders(orders)

    # Проверка класса Dish
    print("\n--- Работа с объектом Dish ---")
    test_dish = Dish(100, "Тест", "Тест", 100.0)
    print("Объект:", test_dish)
    print("is_available()       =", test_dish.is_available())
    print("is_affordable(150)   =", test_dish.is_affordable(150))
    print("Dish.validate_price(0) =", Dish.validate_price(0))

    # Сохранение
    save_dishes(DISHES_FILE, dishes)
    save_categories(CATEGORIES_FILE, categories)
    save_users(USERS_FILE, users)
    save_orders(ORDERS_FILE, orders)


if __name__ == "__main__":
    main()
