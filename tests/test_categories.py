"""Тесты класса Category и функций работы с категориями."""

from models import Category
from models.categories import (
    add_category,
    find_category,
    list_categories,
)


def test_category_creation():
    category = Category(1, "Напитки")
    assert category.id == 1
    assert category.name == "Напитки"
    assert str(category) == "Напитки"


def test_add_category():
    categories = []
    add_category(categories, "Напитки")
    add_category(categories, "Салаты")
    assert len(categories) == 2
    assert categories[0].id == 1
    assert categories[1].id == 2


def test_add_category_no_duplicates():
    categories = []
    add_category(categories, "Напитки")
    add_category(categories, "Напитки")
    assert len(categories) == 1


def test_find_category():
    categories = []
    add_category(categories, "Напитки")
    add_category(categories, "Салаты")
    result = find_category(categories, "нап")
    assert len(result) == 1
    assert result[0].name == "Напитки"


def test_list_categories():
    categories = []
    add_category(categories, "Напитки")
    add_category(categories, "Салаты")
    add_category(categories, "Десерты")
    assert list_categories(categories) == ["Десерты", "Напитки", "Салаты"]
