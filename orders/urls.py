from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("", views.orders, name="orders"),
    path("new/", views.order_form, name="create"),
    path("<int:order_id>/edit/", views.order_form, name="edit"),
    path("<int:order_id>/cancel/", views.order_cancel, name="cancel"),
    path("<int:order_id>/", views.order_detail, name="detail"),
]
