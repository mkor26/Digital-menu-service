from django.db import migrations, models


def populate_slugs(apps, schema_editor):
    Dish = apps.get_model("menu", "Dish")
    dishes = Dish.objects.using(schema_editor.connection.alias)
    for dish in dishes.iterator():
        dish.slug = f"dish-{dish.pk}"
        dish.save(update_fields=["slug"])


class Migration(migrations.Migration):
    dependencies = [("menu", "0001_initial")]
    operations = [
        migrations.AddField("dish", "slug", models.SlugField(blank=True, default=""), preserve_default=False),
        migrations.RunPython(populate_slugs, migrations.RunPython.noop),
        migrations.AlterField("dish", "slug", models.SlugField("Адрес", blank=True, unique=True)),
    ]
