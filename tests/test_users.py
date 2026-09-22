"""Тесты класса User и функций работы с пользователями."""

from models import User
from models.users import add_user, find_user, find_user_by_id


def test_user_creation():
    user = User(1, "Иван Петров", "ivan@example.com")
    assert user.id == 1
    assert user.name == "Иван Петров"
    assert user.email == "ivan@example.com"


def test_user_str():
    user = User(1, "Иван Петров", "ivan@example.com")
    assert "Иван Петров" in str(user)
    assert "ivan@example.com" in str(user)


def test_user_from_data():
    data = {"id": 1, "name": "Иван", "email": "ivan@example.com"}
    user = User.from_data(data)
    assert user.id == 1
    assert user.name == "Иван"


def test_add_user():
    users = []
    add_user(users, "Иван", "ivan@example.com")
    add_user(users, "Мария", "maria@example.com")
    assert len(users) == 2
    assert users[0].id == 1
    assert users[1].id == 2


def test_find_user_by_name():
    users = []
    add_user(users, "Иван Петров", "ivan@example.com")
    add_user(users, "Мария Сидорова", "maria@example.com")
    assert len(find_user(users, "иван")) == 1


def test_find_user_by_email():
    users = []
    add_user(users, "Иван Петров", "ivan@example.com")
    add_user(users, "Мария Сидорова", "maria@example.com")
    assert len(find_user(users, "maria@")) == 1


def test_find_user_by_id():
    users = []
    add_user(users, "Иван", "ivan@example.com")
    user = find_user_by_id(users, 1)
    assert user is not None
    assert user.name == "Иван"
    assert find_user_by_id(users, 99) is None
