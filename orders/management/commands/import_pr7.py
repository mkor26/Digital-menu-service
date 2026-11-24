import sqlite3
from contextlib import closing
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError, transaction

from menu.models import Category, Dish
from orders.models import Customer, Order


TABLES = (
    ("categories", Category, ("id", "name")),
    (
        "dishes", Dish,
        ("id", "name", "category_id", "price", "in_stock", "description"),
    ),
    ("users", Customer, ("id", "name", "email")),
    (
        "orders", Order,
        ("id", "dish_id", "user_id", "quantity", "discount_percent",
         "is_cancelled"),
    ),
)


def build_object(table, model, values):
    if table == "dishes":
        values["slug"] = f"dish-{values['id']}"
    elif table == "orders":
        cancelled = values.pop("is_cancelled")
        values["status"] = (
            Order.Status.CANCELLED if cancelled else Order.Status.ACTIVE
        )
    return model(**values)


class Command(BaseCommand):
    help = "Переносит записи ПР7 в модели Django с сохранением ID и связей."

    def add_arguments(self, parser):
        parser.add_argument(
            "--source", type=Path,
            default=settings.BASE_DIR / "data" / "digital_menu.sqlite",
        )

    def handle(self, *args, **options):
        source = options["source"].resolve()
        try:
            source_uri = f"{source.as_uri()}?mode=ro"
            with closing(sqlite3.connect(source_uri, uri=True)) as db:
                db.execute("BEGIN")
                batches = [
                    (table, model, [
                        build_object(table, model, dict(zip(fields, row)))
                        for row in db.execute(
                            f"SELECT {', '.join(fields)} FROM {table}",
                        )
                    ])
                    for table, model, fields in TABLES
                ]
        except sqlite3.Error as error:
            raise CommandError(
                f"Не удалось прочитать базу ПР7 {source}: {error}",
            ) from error

        try:
            with transaction.atomic():
                if any(model.objects.exists() for _, model, _ in batches):
                    raise CommandError(
                        "Для импорта нужна пустая база предметной области.",
                    )
                for _, model, objects in batches:
                    model.objects.bulk_create(objects)
        except IntegrityError as error:
            raise CommandError(
                f"Импорт отменён из-за нарушения целостности: {error}",
            ) from error

        for table, _, objects in batches:
            self.stdout.write(self.style.SUCCESS(f"{table}: {len(objects)}"))
