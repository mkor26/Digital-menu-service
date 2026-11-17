from django.shortcuts import render

from db.database import get_statistics


def index(request):
    return render(request, "homepage/index.html")


def statistics(request):
    summary, categories, orders_count = get_statistics()
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
