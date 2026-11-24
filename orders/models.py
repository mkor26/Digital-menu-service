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


class OrderStatus(models.TextChoices):
    ACTIVE = "active", "Активен"
    CANCELLED = "cancelled", "Отменён"
    COMPLETED = "completed", "Завершён"


class OrderQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=OrderStatus.ACTIVE)

    def cancelled(self):
        return self.filter(status=OrderStatus.CANCELLED)

    def completed(self):
        return self.filter(status=OrderStatus.COMPLETED)

    def for_date(self, day):
        return self.filter(order_date=day)


class Order(models.Model):
    Status = OrderStatus
    objects = OrderQuerySet.as_manager()
    dish = models.ForeignKey(
        "menu.Dish", on_delete=models.PROTECT, related_name="orders",
    )
    user = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="orders",
    )
    quantity = models.PositiveIntegerField("количество", default=1)
    discount_percent = models.FloatField("скидка, %", default=0)
    status = models.CharField(
        "Статус", max_length=10, choices=Status.choices,
        default=Status.ACTIVE, db_index=True,
    )
    order_date = models.DateField("Дата предзаказа", null=True, blank=True)

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
            models.UniqueConstraint(
                fields=["dish", "order_date"],
                condition=models.Q(status="active", order_date__isnull=False),
                name="one_active_preorder_per_dish_and_date",
            ),
        ]

    def cancel(self):
        if (
            type(self)
            .objects.active()
            .filter(pk=self.pk)
            .update(status=self.Status.CANCELLED)
        ):
            self.status = self.Status.CANCELLED

    def __str__(self):
        return f"Заказ №{self.pk}"
