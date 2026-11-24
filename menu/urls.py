from django.urls import path

from . import views

app_name = "menu"

urlpatterns = [
    path("", views.dishes, name="dishes"),
    path("<int:dish_id>/", views.dish_detail, name="detail"),
    path("dish/<slug:slug>/image/", views.dish_image, name="image"),
    path("dish/<slug:slug>/", views.dish_detail, name="detail_slug"),
]
