import re

from django.core.paginator import Paginator
from django.db.models import F
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Order, order_total


ORDER_SORTS = {
    "id": ("id",),
    "-id": ("-id",),
    "dish": ("dish__name", "id"),
    "total": ("total", "id"),
}


def orders(request):
    search = request.GET.get("q", "").strip()
    customer = request.GET.get("customer", "").strip()
    status = request.GET.get("status", "")
    sort = request.GET.get("sort", "id")
    if sort not in ORDER_SORTS:
        sort = "id"

    queryset = Order.objects.all()
    if search:
        queryset = queryset.filter(dish__name__iregex=re.escape(search))
    if customer:
        queryset = queryset.filter(user__name__iregex=re.escape(customer))
    if status == "active":
        queryset = queryset.exclude(is_cancelled=True)
    elif status == "cancelled":
        queryset = queryset.filter(is_cancelled=True)

    rows = queryset.annotate(
        dish_name=F("dish__name"),
        user_name=F("user__name"),
        total=order_total(),
    ).values("id", "dish_name", "user_name", "is_cancelled", "total")
    page_obj = Paginator(rows.order_by(*ORDER_SORTS[sort]), 5).get_page(
        request.GET.get("page"),
    )
    return render(
        request, "orders/order_list.html",
        {
            "orders": page_obj,
            "page_obj": page_obj,
            "search": search,
            "customer": customer,
            "status_filter": status,
            "sort": sort,
        },
    )


def order_detail(request, order_id):
    queryset = Order.objects.select_related("dish", "user").annotate(
        total=order_total(),
    )
    try:
        order = get_object_or_404(queryset, pk=order_id)
    except Http404:
        return render(request, "orders/order_detail.html", status=404)
    return render(request, "orders/order_detail.html", {"order": order})
