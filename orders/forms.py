from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Order

ORDER_SORT_OPTIONS = {
    "id": ("По номеру", ("id",)),
    "-id": ("По номеру, убывание", ("-id",)),
    "dish": ("По блюду", ("dish__name", "id")),
    "total": ("По сумме", ("total", "id")),
    "newest": ("Сначала новые даты", ("-order_date", "-pk")),
    "oldest": ("Сначала ранние даты", ("order_date", "pk")),
    "quantity": ("По количеству", ("-quantity", "-pk")),
}
SORTS = {key: fields for key, (_, fields) in ORDER_SORT_OPTIONS.items()}


class OrderFilterForm(forms.Form):
    date = forms.DateField(
        label="Дата предзаказа",
        required=False,
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-control"}
        ),
    )
    dish = forms.CharField(
        label="Блюдо",
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    customer = forms.CharField(
        label="Клиент",
        required=False,
        max_length=160,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    status = forms.ChoiceField(
        label="Статус",
        required=False,
        choices=[("", "Все статусы"), *Order.Status.choices],
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    sort = forms.ChoiceField(
        label="Сортировка",
        required=False,
        choices=[
            (key, label) for key, (label, _) in ORDER_SORT_OPTIONS.items()
        ],
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class OrderForm(forms.ModelForm):
    order_date = forms.DateField(
        label="Дата предзаказа",
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={"type": "date", "class": "form-control"},
        ),
        help_text="Выберите сегодняшнюю или будущую дату.",
    )

    quantity = forms.IntegerField(
        label="Количество", min_value=1, max_value=2147483647,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    discount_percent = forms.FloatField(
        label="Скидка (%)", min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Order
        fields = ("dish", "user", "order_date", "quantity", "discount_percent")
        widgets = {
            "dish": forms.Select(attrs={"class": "form-select"}),
            "user": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_order_date(self):
        day = self.cleaned_data["order_date"]
        if day < timezone.localdate():
            raise ValidationError("Дата предзаказа не может быть в прошлом.")
        return day

    def occupied(self):
        dish = self.cleaned_data["dish"]
        day = self.cleaned_data["order_date"]
        return (
            Order.objects.active()
            .for_date(day)
            .filter(dish=dish)
            .exclude(pk=self.instance.pk)
            .exists()
        )

    def clean(self):
        data = super().clean()
        dish = data.get("dish")
        if dish and not dish.in_stock:
            self.add_error("dish", "Этого блюда сейчас нет в наличии.")
        elif dish and data.get("order_date") and self.occupied():
            raise ValidationError(
                "На эту дату уже есть активный предзаказ блюда."
            )
        return data
