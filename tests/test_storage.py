"""Тесты для функций сохранения и загрузки данных."""

import json
import os

from storage import load_dishes, save_dishes


def test_save_and_load_dishes(tmp_path):
    filename = os.path.join(tmp_path, "dishes.json")
    dishes = [
        {"id": 1, "name": "Капучино", "price": 250.0, "in_stock": True},
        {"id": 2, "name": "Цезарь", "price": 450.0, "in_stock": True},
    ]

    save_dishes(filename, dishes)
    loaded = load_dishes(filename)

    assert loaded == dishes


def test_load_dishes_missing_file(tmp_path, capsys):
    filename = os.path.join(tmp_path, "missing.json")
    result = load_dishes(filename)

    assert result == []
    captured = capsys.readouterr()
    assert "не найден" in captured.out


def test_load_dishes_broken_json(tmp_path, capsys):
    filename = os.path.join(tmp_path, "broken.json")
    with open(filename, "w", encoding="utf-8") as file:
        file.write("{это не JSON}")

    result = load_dishes(filename)
    assert result == []
    captured = capsys.readouterr()
    assert "Не удалось прочитать" in captured.out