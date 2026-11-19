from django.db.models import Avg, Count, F, Max, Min, Q
from django.db.models.functions import Round
from django.shortcuts import render

from menu.models import Category, Dish
from orders.models import Order


def index(request):
    return render(request, "homepage/index.html")


def statistics(request):
    summary = Dish.objects.aggregate(
        dishes_count=Count("pk"),
        available_count=Count("pk", filter=Q(in_stock=True)),
        min_price=Min("price"),
        max_price=Max("price"),
        average_price=Round(Avg("price"), precision=2),
    )
    categories = Category.objects.annotate(
        category=F("name"), dishes_count=Count("dishes"),
    ).values("category", "dishes_count").order_by("name")
    orders_count = Order.objects.aggregate(
        orders_count=Count("pk"),
        active_orders=Count("pk", filter=Q(is_cancelled=False)),
    )
    return render(
        request,
        "homepage/statistics.html",
        {
            "summary": summary,
            "categories": categories,
            "orders_count": orders_count,
        },
    )


def page_not_found(request, exception):
    return render(request, "404.html", status=404)
