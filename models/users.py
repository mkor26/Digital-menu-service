"""Класс User и функции работы с коллекцией пользователей."""


class User:
    """Пользователь системы (посетитель или официант)."""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        """Создать объект пользователя."""
        self.id = user_id
        self.name = name
        self.email = email

    def __str__(self) -> str:
        """Вернуть строковое представление пользователя."""
        return f"{self.name} <{self.email}>"

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать пользователя из словаря."""
        return cls(
            user_id=data["id"],
            name=data["name"],
            email=data["email"],
        )

    def to_data(self) -> dict:
        """Преобразовать пользователя в словарь для JSON."""
        return {"id": self.id, "name": self.name, "email": self.email}


def add_user(users: list[User], name: str, email: str) -> User:
    """Создать пользователя и добавить его в коллекцию."""
    if users:
        new_id = max(user.id for user in users) + 1
    else:
        new_id = 1

    user = User(new_id, name, email)
    users.append(user)
    return user


def find_user(users: list[User], query: str) -> list[User]:
    """Найти пользователей по имени или email (без учёта регистра)."""
    query_lower = query.lower()
    result: list[User] = []
    for user in users:
        in_name = query_lower in user.name.lower()
        in_email = query_lower in user.email.lower()
        if in_name or in_email:
            result.append(user)
    return result


def find_user_by_id(users: list[User], user_id: int) -> User | None:
    """Найти пользователя по идентификатору."""
    for user in users:
        if user.id == user_id:
            return user
    return None


def show_users(users: list[User]) -> None:
    """Напечатать пользователей."""
    if not users:
        print("Список пользователей пуст.")
        return
    for user in users:
        print(" -", user)
