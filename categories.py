"""Модуль для работы с категориями меню."""


def add_category(categories: list[dict], name: str) -> dict:
    """Добавить категорию в список и вернуть её словарь.

    Если категория с таким названием уже существует — вернуть её.
    """
    for category in categories:
        if category["name"] == name:
            return category

    if categories:
        new_id = max(category["id"] for category in categories) + 1
    else:
        new_id = 1

    category = {"id": new_id, "name": name}
    categories.append(category)
    return category


def find_category(categories: list[dict], query: str) -> list[dict]:
    """Найти категории по подстроке названия (без учёта регистра)."""
    query_lower = query.lower()
    return [c for c in categories if query_lower in c["name"].lower()]


def list_categories(categories: list[dict]) -> list[str]:
    """Вернуть отсортированный список названий категорий."""
    return sorted(category["name"] for category in categories)