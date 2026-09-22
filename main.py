from dishes import (
    add_dish,
    calculate_order,
    check_availability,
    filter_dishes_by_category,
    filter_dishes_by_price,
    find_dish,
    show_dish,
    sort_dishes,
)
from categories import add_category, list_categories
from storage import (
    load_categories,
    load_dishes,
    save_categories,
    save_dishes,
)


DISHES_FILE = "data/dishes.json"
CATEGORIES_FILE = "data/categories.json"


def show_dishes(dishes: list[dict]) -> None:  #Напечатать список блюд
    if not dishes:
        print("Список блюд пуст.")
        return
    for dish in dishes:
        print(" -", show_dish(dish))


def main() -> None:
    print("=== Электронное меню ===")

    # Загрузка данных из файлов
    dishes = load_dishes(DISHES_FILE)
    categories = load_categories(CATEGORIES_FILE)

    # Если файлов ещё нет — создаём стартовые данные
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
        save_dishes(DISHES_FILE, dishes)

    if not categories:
        add_category(categories, "Напитки")
        add_category(categories, "Салаты")
        add_category(categories, "Десерты")
        save_categories(CATEGORIES_FILE, categories)

    # Демонстрация возможностей
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
    for name in list_categories(categories):
        print(" *", name)

    # Демонстрация функции из ПР1
    dish = dishes[0]
    print("\n--- Карточка блюда и заказ ---")
    print(show_dish(dish))
    print(check_availability(dish))
    total = calculate_order(dish, quantity=2, discount_percent=10.0)
    print(f"Итого к оплате: {total:.2f} руб.")

    # Сохраняем актуальное состояние
    save_dishes(DISHES_FILE, dishes)
    save_categories(CATEGORIES_FILE, categories)


if __name__ == "__main__":
    main()