from django.db import migrations, models


def migrate_status(apps, schema_editor):
    orders = apps.get_model("orders", "Order").objects.using(schema_editor.connection.alias)
    orders.filter(is_cancelled=True).update(status="cancelled")
    orders.filter(is_cancelled=False).update(status="active")


def restore_flag(apps, schema_editor):
    orders = apps.get_model("orders", "Order").objects.using(schema_editor.connection.alias)
    orders.filter(status="cancelled").update(is_cancelled=True)


class Migration(migrations.Migration):
    dependencies = [("orders", "0001_initial")]
    operations = [
        migrations.AddField(
            "order", "order_date",
            models.DateField("Дата предзаказа", null=True, blank=True),
        ),
        migrations.AddField(
            "order", "status",
            models.CharField(
                "Статус", max_length=10, db_index=True, default="active",
                choices=[("active", "Активен"), ("cancelled", "Отменён"), ("completed", "Завершён")],
            ),
        ),
        migrations.RunPython(migrate_status, restore_flag),
        migrations.RemoveField("order", "is_cancelled"),
        migrations.AddConstraint(
            "order", models.UniqueConstraint(
                fields=["dish", "order_date"], condition=models.Q(status="active", order_date__isnull=False),
                name="one_active_preorder_per_dish_and_date",
            ),
        ),
    ]
