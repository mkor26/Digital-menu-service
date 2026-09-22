"""Модуль сохранения и загрузки данных проекта в JSON-файлах."""

import json
import os


def load_dishes(filename: str) -> list[dict]:
    """Загрузить список блюд из JSON-файла.

    Если файл отсутствует или содержит некорректный JSON —
    вернуть пустой список и напечатать предупреждение.
    """
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден, будет создан новый.")
        return []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        print(f"Не удалось прочитать {filename}: {error}")
        return []


def save_dishes(filename: str, dishes: list[dict]) -> None:
    """Сохранить список блюд в JSON-файл."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(dishes, file, ensure_ascii=False, indent=4)
    except OSError as error:
        print(f"Не удалось сохранить {filename}: {error}")


def load_categories(filename: str) -> list[dict]:
    """Загрузить список категорий из JSON-файла."""
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден, будет создан новый.")
        return []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        print(f"Не удалось прочитать {filename}: {error}")
        return []


def save_categories(filename: str, categories: list[dict]) -> None:
    """Сохранить список категорий в JSON-файл."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(categories, file, ensure_ascii=False, indent=4)
    except OSError as error:
        print(f"Не удалось сохранить {filename}: {error}")