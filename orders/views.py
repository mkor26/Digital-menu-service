"""Представления заказов, использующие SQL JOIN для связанных данных."""

from django.shortcuts import render

from db.database import get_order, get_orders


def orders(request):
    return render(request, "orders/order_list.html", {"orders": get_orders()})


def order_detail(request, order_id):
    order = get_order(order_id)
    return render(
        request,
        "orders/order_detail.html",
        {"order": order},
        status=404 if order is None else 200,
    )
