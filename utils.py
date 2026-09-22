"""Вспомогательные функции безопасного ввода."""

from datetime import date, datetime


DATE_FORMAT = "%d.%m.%Y"


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число, повторяя запрос при ошибке."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: нужно ввести целое число. Попробуйте снова.")


def input_float(prompt: str) -> float:
    """Запросить у пользователя число с плавающей точкой."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: нужно ввести число. Попробуйте снова.")


def input_date(prompt: str) -> date:
    """Запросить у пользователя дату в формате ДД.ММ.ГГГГ."""
    while True:
        try:
            return datetime.strptime(input(prompt), DATE_FORMAT).date()
        except ValueError:
            print(f"Ошибка: дата должна быть в формате {DATE_FORMAT}.")
