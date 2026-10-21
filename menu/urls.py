from django.urls import path

from . import views

app_name = "menu"

urlpatterns = [
    path("", views.dishes, name="dishes"),
    path("<int:dish_id>/", views.dish_detail, name="detail"),
]
