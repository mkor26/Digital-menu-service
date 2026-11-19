from django.contrib import admin

from .models import Customer, Order


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "email")
    search_fields = ("name", "email")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "dish", "user", "quantity", "is_cancelled")
    list_filter = ("is_cancelled",)
    search_fields = ("dish__name", "user__name", "user__email")
    list_select_related = ("dish", "user")
