from django import forms

from .models import Dish


class DishImageForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ("image",)
        widgets = {
            "image": forms.ClearableFileInput(attrs={"class": "form-control"})
        }
