"""Класс Category и функции работы с коллекцией категорий."""


class Category:
    """Категория меню (например, «Напитки», «Салаты»)."""

    def __init__(self, category_id: int, name: str) -> None:
        """Создать объект категории."""
        self.id = category_id
        self.name = name

    def __str__(self) -> str:
        """Вернуть строковое представление категории."""
        return self.name

    @classmethod
    def from_data(cls, data: dict) -> "Category":
        """Создать категорию из словаря."""
        return cls(category_id=data["id"], name=data["name"])

    def to_data(self) -> dict:
        """Преобразовать категорию в словарь для JSON."""
        return {"id": self.id, "name": self.name}


def add_category(categories: list[Category], name: str) -> Category:
    """Добавить категорию, если её ещё нет. Вернуть существующую или новую."""
    for category in categories:
        if category.name == name:
            return category

    if categories:
        new_id = max(category.id for category in categories) + 1
    else:
        new_id = 1

    category = Category(new_id, name)
    categories.append(category)
    return category


def find_category(
    categories: list[Category], query: str
) -> list[Category]:
    """Найти категории по подстроке названия (без учёта регистра)."""
    query_lower = query.lower()
    return [c for c in categories if query_lower in c.name.lower()]


def list_categories(categories: list[Category]) -> list[str]:
    """Вернуть отсортированный список названий категорий."""
    return sorted(category.name for category in categories)


def show_categories(categories: list[Category]) -> None:
    """Напечатать категории меню."""
    if not categories:
        print("Список категорий пуст.")
        return
    for category in sorted(categories, key=lambda c: c.name):
        print(" *", category)
