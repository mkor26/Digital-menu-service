from django.contrib import admin

from .models import Customer, Order


class OrderInline(admin.TabularInline):
    model = Order
    extra = 0


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "email")
    search_fields = ("name", "email")
    ordering = ("name", "pk")
    inlines = (OrderInline,)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "dish", "user", "order_date", "quantity", "status")
    list_select_related = ("dish", "user")
    search_fields = ("dish__name", "user__name", "user__email")
    list_filter = ("status", "order_date", "dish__category")
    ordering = ("-order_date", "-pk")
    list_per_page = 20
