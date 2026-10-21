from django.shortcuts import render
from models.dishes import find_dish_by_id
from storage import load_all


def dishes(request):
    dishes_list, _, _ = load_all()
    return render(request, "menu/dish_list.html", {"dishes": dishes_list})


def dish_detail(request, dish_id):
    dishes_list, _, _ = load_all()
    dish = find_dish_by_id(dishes_list, dish_id)

    return render(
        request,
        "menu/dish_detail.html",
        {"dish": dish},
        status=404 if dish is None else 200
    )