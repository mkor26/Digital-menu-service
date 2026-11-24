from uuid import uuid4

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


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
    image = models.ImageField("Фото", upload_to="dishes/", blank=True)
    slug = models.SlugField("Адрес", blank=True, unique=True)

    class Meta:
        verbose_name = "блюдо"
        verbose_name_plural = "блюда"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="dish_nonnegative_price",
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            prefix = slugify(self.name)[:35] or "dish"
            self.slug = f"{prefix}-{uuid4().hex[:12]}"
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("menu:detail_slug", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name
