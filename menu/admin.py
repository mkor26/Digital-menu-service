from django.contrib import admin

from .models import Category, Dish


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "in_stock")
    list_filter = ("category", "in_stock")
    search_fields = ("name", "description")
    list_select_related = ("category",)
