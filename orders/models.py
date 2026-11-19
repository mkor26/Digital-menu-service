from django.db import models
from django.db.models.functions import Round


class Customer(models.Model):
    name = models.CharField("имя", max_length=150)
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = "покупатель"
        verbose_name_plural = "покупатели"

    def __str__(self):
        return self.name


def order_total():
    return Round(
        models.F("dish__price") * models.F("quantity")
        * (1 - models.F("discount_percent") / 100.0),
        precision=2,
    )


class Order(models.Model):
    dish = models.ForeignKey(
        "menu.Dish", on_delete=models.PROTECT, related_name="orders",
    )
    user = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="orders",
    )
    quantity = models.PositiveIntegerField("количество", default=1)
    discount_percent = models.FloatField("скидка, %", default=0)
    is_cancelled = models.BooleanField("отменён", default=False)

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantity__gt=0),
                name="order_positive_quantity",
            ),
            models.CheckConstraint(
                condition=models.Q(discount_percent__range=(0, 100)),
                name="order_discount_range",
            ),
        ]

    def __str__(self):
        return f"Заказ №{self.pk}"
