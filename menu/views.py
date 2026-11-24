import re
from datetime import date
from math import isfinite

from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from orders.models import Order

from .forms import DishImageForm

from .models import Category, Dish


MENU_SORTS = {
    "name": ("name", "pk"),
    "price": ("price", "name", "pk"),
    "-price": ("-price", "name", "pk"),
    "category": ("category__name", "name", "pk"),
}


def dishes(request):
    try:
        category_id = int(request.GET.get("category", ""))
        if not 0 < category_id <= 2**63 - 1:
            category_id = None
    except ValueError:
        category_id = None

    try:
        max_price = float(request.GET.get("max_price", ""))
        if not isfinite(max_price) or max_price < 0:
            max_price = None
    except ValueError:
        max_price = None

    available_only = request.GET.get("available") == "1"
    search = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "name")
    if sort not in MENU_SORTS:
        sort = "name"

    queryset = Dish.objects.select_related("category")
    if category_id is not None and max_price is not None:
        queryset = queryset.filter(
            category_id=category_id, price__lte=max_price,
        )
    elif category_id is not None:
        queryset = queryset.filter(category_id=category_id)
    elif max_price is not None:
        queryset = queryset.filter(price__lte=max_price)
    if available_only:
        queryset = queryset.exclude(in_stock=False)
    if search:
        pattern = re.escape(search)
        queryset = queryset.filter(
            Q(name__iregex=pattern) | Q(description__iregex=pattern),
        )

    day = request.GET.get("date", "")
    date_error = False
    if day:
        try:
            selected_date = date.fromisoformat(day)
        except ValueError:
            date_error = True
        else:
            booked = (
                Order.objects.active().for_date(selected_date)
                .values_list("dish_id", flat=True)
            )
            queryset = queryset.filter(in_stock=True).exclude(pk__in=booked)

    page_obj = Paginator(queryset.order_by(*MENU_SORTS[sort]), 5).get_page(
        request.GET.get("page"),
    )
    return render(
        request,
        "menu/dish_list.html",
        {
            "dishes": page_obj,
            "page_obj": page_obj,
            "categories": Category.objects.order_by("name"),
            "selected_category": category_id,
            "max_price": max_price,
            "available_only": available_only,
            "search": search,
            "sort": sort,
            "date": day,
            "date_error": date_error,
        },
    )


def dish_detail(request, dish_id=None, slug=None):
    lookup = {"pk": dish_id} if dish_id is not None else {"slug": slug}
    try:
        dish = get_object_or_404(
            Dish.objects.select_related("category"), **lookup,
        )
    except Http404:
        return render(request, "menu/dish_detail.html", status=404)
    return render(request, "menu/dish_detail.html", {"dish": dish})


@staff_member_required
@require_http_methods(["GET", "POST"])
def dish_image(request, slug):
    dish = get_object_or_404(Dish, slug=slug)
    form = DishImageForm(instance=dish)
    if request.method == "POST":
        form = DishImageForm(request.POST, request.FILES, instance=dish)
        if form.is_valid():
            form.save()
            return redirect(dish)
    return render(
        request,
        "form.html",
        {"form": form, "title": f"Фото блюда «{dish.name}»"},
    )
