from django.db import models


class Category(models.Model):
    name = models.CharField("название", max_length=150, unique=True)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField("название", max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="dishes",
    )
    price = models.FloatField("цена")
    in_stock = models.BooleanField("в наличии", default=True)
    description = models.TextField("описание", blank=True, default="")

    class Meta:
        verbose_name = "блюдо"
        verbose_name_plural = "блюда"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="dish_nonnegative_price",
            ),
        ]

    def __str__(self):
        return self.name
