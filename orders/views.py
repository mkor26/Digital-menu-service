import re

from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.db.models import F
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from .forms import SORTS, OrderFilterForm, OrderForm
from .models import Order, order_total


def orders(request):
    params = request.GET
    filters_data = params.copy()
    if "dish" not in filters_data and "q" in filters_data:
        filters_data["dish"] = filters_data["q"]
    form = OrderFilterForm(filters_data or None)
    queryset = Order.objects.all()
    if form.is_bound and form.is_valid():
        filters = form.cleaned_data
        if filters["date"]:
            queryset = queryset.for_date(filters["date"])
        if filters["dish"]:
            queryset = queryset.filter(
                dish__name__iregex=re.escape(filters["dish"])
            )
        if filters["customer"]:
            queryset = queryset.filter(
                user__name__iregex=re.escape(filters["customer"])
            )
        if filters["status"]:
            queryset = queryset.filter(status=filters["status"])
        elif params.get("active") == "1":
            queryset = queryset.active()
        ordering = SORTS.get(filters["sort"], SORTS["id"])
    else:
        ordering = SORTS["id"]
        if form.is_bound:
            queryset = queryset.none()
    rows = (
        queryset.annotate(
            dish_name=F("dish__name"),
            user_name=F("user__name"),
            total=order_total(),
        )
        .order_by(*ordering)
        .values(
            "id",
            "dish_name",
            "user_name",
            "order_date",
            "quantity",
            "status",
            "total",
        )
    )
    page = Paginator(rows, 5).get_page(params.get("page"))
    return render(
        request,
        "orders/order_list.html",
        {
            "orders": page,
            "page_obj": page,
            "form": form,
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


@staff_member_required
@require_http_methods(["GET", "POST"])
def order_form(request, order_id=None):
    order = (
        get_object_or_404(Order.objects.active(), pk=order_id)
        if order_id is not None
        else None
    )
    data = request.POST if request.method == "POST" else None
    form = OrderForm(data, instance=order)
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                if order is None:
                    saved = form.save()
                else:
                    saved = form.save(commit=False)
                    changed = (
                        Order.objects.active()
                        .filter(pk=saved.pk)
                        .update(
                            dish=saved.dish,
                            user=saved.user,
                            order_date=saved.order_date,
                            quantity=saved.quantity,
                            discount_percent=saved.discount_percent,
                        )
                    )
                    if not changed:
                        raise Http404("Активный предзаказ не найден.")
        except IntegrityError:
            if not form.occupied():
                raise
            form.add_error(
                None, "На эту дату уже есть активный предзаказ блюда."
            )
        else:
            return redirect("orders:detail", order_id=saved.pk)
    title = "Изменить предзаказ" if order else "Новый предзаказ"
    return render(request, "form.html", {"form": form, "title": title})


@require_POST
@staff_member_required
def order_cancel(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.cancel()
    return redirect("orders:detail", order_id=order.pk)
