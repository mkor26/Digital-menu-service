from datetime import timedelta
from decimal import Decimal
from io import BytesIO
from tempfile import TemporaryDirectory

from PIL import Image

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError, transaction
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from menu.models import Category, Dish

from .models import Customer, Order, order_total


class DmsScenarios(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Тестовое меню")
        cls.dish = Dish.objects.create(
            name="Тестовый суп",
            category=cls.category,
            price=Decimal("100.00"),
        )
        cls.customer = Customer.objects.create(
            name="Тестовый клиент",
            email="test-customer@example.com",
        )
        cls.staff = get_user_model().objects.create_superuser("dms-test")
        cls.day = timezone.localdate() + timedelta(days=1)

    def form_data(self, **changes):
        return {
            "dish": self.dish.pk,
            "user": self.customer.pk,
            "order_date": self.day.isoformat(),
            "quantity": 2,
            "discount_percent": "15",
            **changes,
        }

    def test_create_edit_conflict_cancel_and_rebook(self):
        self.client.force_login(self.staff)
        create = reverse("orders:create")
        self.assertContains(self.client.get(create), "Новый предзаказ")
        response = self.client.post(create, self.form_data())
        order = self.customer.orders.get(dish=self.dish)
        self.assertRedirects(
            response, reverse("orders:detail", args=[order.pk])
        )
        saved = Order.objects.annotate(total=order_total()).get(pk=order.pk)
        self.assertEqual(saved.total, 170)
        listing = self.client.get(
            reverse("orders:orders"), {"dish": self.dish.name}
        )
        self.assertEqual(listing.context["orders"][0]["total"], 170)
        menu = reverse("menu:dishes")
        self.assertNotContains(
            self.client.get(menu, {"date": self.day}), self.dish.name
        )
        conflict = self.client.post(create, self.form_data())
        self.assertContains(conflict, "уже есть активный предзаказ")
        edit = reverse("orders:edit", args=[order.pk])
        self.assertEqual(
            self.client.post(edit, self.form_data(quantity=3)).status_code, 302
        )
        self.assertEqual(self.customer.orders.get(pk=order.pk).quantity, 3)
        cancel = reverse("orders:cancel", args=[order.pk])
        self.assertEqual(self.client.get(cancel).status_code, 405)
        self.assertEqual(self.client.post(cancel).status_code, 302)
        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.CANCELLED)
        self.assertContains(
            self.client.get(menu, {"date": self.day}), self.dish.name
        )
        self.assertEqual(
            self.client.post(create, self.form_data()).status_code, 302
        )

    def test_invalid_input_and_csrf(self):
        create = reverse("orders:create")
        self.assertEqual(self.client.get(create).status_code, 302)
        self.client.force_login(self.staff)
        response = self.client.post(
            create,
            self.form_data(
                order_date=(
                    timezone.localdate() - timedelta(days=1)
                ).isoformat(),
                quantity=0,
            ),
        )
        self.assertContains(response, "не может быть в прошлом")
        self.assertIn("quantity", response.context["form"].errors)
        self.assertFalse(self.customer.orders.exists())
        strict = Client(enforce_csrf_checks=True)
        strict.force_login(self.staff)
        self.assertEqual(
            strict.post(create, self.form_data()).status_code, 403
        )
        strict.get(create)
        cookies = strict.cookies["csrftoken"]
        self.assertEqual(
            strict.post(
                create,
                self.form_data(),
                headers={"X-CSRFToken": cookies.value},
            ).status_code,
            302,
        )
        self.assertEqual(
            self.client.get(reverse("orders:edit", args=[999999])).status_code,
            404,
        )

    def test_order_filter_pagination_and_ordering(self):
        for quantity in range(1, 8):
            Order.objects.create(
                dish=self.dish,
                user=self.customer,
                quantity=quantity,
                status=Order.Status.COMPLETED,
                order_date=self.day,
            )
        url = reverse("orders:orders")
        query = {
            "dish": self.dish.name,
            "date": self.day.isoformat(),
            "sort": "quantity",
            "status": "completed",
        }
        first = self.client.get(url, query)
        self.assertEqual(first.context["page_obj"].paginator.count, 7)
        self.assertEqual(
            [row["quantity"] for row in first.context["orders"]],
            [7, 6, 5, 4, 3],
        )
        self.assertContains(
            first, "sort=quantity&amp;status=completed&amp;page=2"
        )
        second = self.client.get(url, {**query, "page": 2})
        self.assertEqual(
            [row["quantity"] for row in second.context["orders"]], [2, 1]
        )
        invalid = self.client.get(url, {"date": "invalid", "sort": "unknown"})
        self.assertEqual(set(invalid.context["form"].errors), {"date", "sort"})
        self.assertEqual(invalid.context["page_obj"].paginator.count, 0)
        self.assertTrue(
            Order.objects.completed().filter(dish=self.dish).exists()
        )

    def test_unique_active_preorder(self):
        order_data = {
            "dish": self.dish,
            "user": self.customer,
            "order_date": self.day,
        }
        Order.objects.create(**order_data)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Order.objects.create(**order_data)

    def test_upload_and_render_image(self):
        self.client.force_login(self.staff)
        url = reverse("menu:image", args=[self.dish.slug])
        self.assertContains(
            self.client.get(url), 'enctype="multipart/form-data"'
        )
        self.assertContains(
            self.client.get(self.dish.get_absolute_url()), "Фотография блюда"
        )
        with TemporaryDirectory() as media, self.settings(MEDIA_ROOT=media):
            invalid = SimpleUploadedFile(
                "bad.png", b"invalid", content_type="image/png"
            )
            self.assertIn(
                "image",
                self.client.post(url, {"image": invalid})
                .context["form"]
                .errors,
            )
            image = BytesIO()
            Image.new("RGB", (4, 4), "red").save(image, format="PNG")
            uploaded = SimpleUploadedFile(
                "dish.png", image.getvalue(), content_type="image/png"
            )
            self.assertEqual(
                self.client.post(url, {"image": uploaded}).status_code, 302
            )
            self.dish.refresh_from_db()
            self.assertTrue(
                self.dish.image.storage.exists(self.dish.image.name)
            )
            page = self.client.get(self.dish.get_absolute_url())
            self.assertContains(page, self.dish.image.url)

    def test_admin_pages_and_statistics(self):
        self.client.force_login(self.staff)
        for url in (
            reverse("admin:menu_dish_changelist"),
            reverse("admin:orders_customer_change", args=[self.customer.pk]),
            reverse("admin:orders_order_changelist") + "?status__exact=active",
            reverse("homepage:statistics"),
        ):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_admin_can_replace_a_dish_photo(self):
        self.client.force_login(self.staff)
        url = reverse("admin:menu_dish_change", args=[self.dish.pk])
        with TemporaryDirectory() as media, self.settings(MEDIA_ROOT=media):
            for number, color in enumerate(("red", "blue"), start=1):
                content = BytesIO()
                Image.new("RGB", (4, 4), color).save(content, format="PNG")
                name = f"test-{number}.png"
                upload = SimpleUploadedFile(
                    name, content.getvalue(), content_type="image/png",
                )
                response = self.client.post(url, {
                    "name": self.dish.name,
                    "category": self.category.pk,
                    "price": str(self.dish.price),
                    "slug": self.dish.slug,
                    "in_stock": "on",
                    "image": upload,
                    "_save": "Save",
                })
                self.assertEqual(response.status_code, 302)
                self.dish.refresh_from_db()
                self.assertTrue(self.dish.image.name.endswith(name))
                with self.dish.image.open("rb") as file:
                    self.assertEqual(file.read(), content.getvalue())
                self.assertContains(
                    self.client.get(self.dish.get_absolute_url()),
                    self.dish.image.url,
                )
