"""Представления меню, получающие данные непосредственно из SQLite."""

from django.shortcuts import render

from db.database import get_categories, get_dish, get_dishes


def dishes(request):
    category_id = request.GET.get("category") or None
    max_price = request.GET.get("max_price") or None
    available_only = request.GET.get("available") == "1"

    try:
        category_id = int(category_id) if category_id else None
    except ValueError:
        category_id = None

    try:
        max_price = float(max_price) if max_price else None
        if max_price is not None and max_price < 0:
            max_price = None
    except ValueError:
        max_price = None

    dishes_list = get_dishes(category_id, max_price, available_only)
    return render(
        request,
        "menu/dish_list.html",
        {
            "dishes": dishes_list,
            "categories": get_categories(),
            "selected_category": category_id,
            "max_price": max_price,
            "available_only": available_only,
        },
    )


def dish_detail(request, dish_id):
    dish = get_dish(dish_id)
    return render(
        request,
        "menu/dish_detail.html",
        {"dish": dish},
        status=404 if dish is None else 200,
    )
