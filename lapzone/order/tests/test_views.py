import json
from datetime import datetime

import pytz
from django.conf import settings
from django.test import TestCase
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.contrib.messages import get_messages

from order.models import Order, OrderItem
from order.forms import OrderCheckoutModelForm
from shop.models import Brand, Category, Product
from general.test_mixins.for_views import (
    ViewTestMixin,
    UserTestMixin,
    ProductTestMixin,
    LoginRequiredTestMixin,
    DeleteViewTestMixin,
)


class OrderCheckoutFormViewTestCase(ProductTestMixin, ViewTestMixin, TestCase):
    """Tests for the OrderCheckoutFormView."""

    url = "/order/checkout/"
    name = "order:create"
    template_name = "order/order_checkout.html"

    @classmethod
    def setUpTestData(cls) -> None:
        """Creates a user and a product for testing the order checkout page."""
        super().setUpTestData()
        cls.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass",
            first_name="Test",
            last_name="User",
        )

    def test_order_checkout_page_message_with_empty_cart(self):
        """
        Test that the order checkout page with empty cart has correct message.
        """
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(
            self.response, "There are no products in your cart yet."
        )

    def test_checkout_form_is_on_page(self):
        """Test that the "form" there is on a page."""
        self.assertIn("form", self.response.context)
        self.assertIsInstance(
            self.response.context["form"], OrderCheckoutModelForm
        )

    def test_checkout_form_is_create_profile_field_if_user_authenticated(self):
        """
        Test that the checkout form does not have the "is_create_profile" field if user is authenticated.
        """
        User.objects.create_user(
            username="testuser2", email="test2@test.com", password="testpass"
        )
        self.client.login(username="testuser2", password="testpass")
        response = self.client.get(self.url)
        self.assertFalse(
            response.context["form"].fields.get("is_create_profile", False)
        )

    def test_checkout_form_does_not_have_filled_user_fields(self):
        """Test that the checkout form does not have filled user fields."""
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        form = response.context["form"]
        self.assertFalse(form.fields.get("email", False))
        self.assertFalse(form.fields.get("first_name", False))
        self.assertFalse(form.fields.get("last_name", False))

    def test_order_checkout_if_user_is_not_authenticated_and_do_not_want_to_create_profile(
        self,
    ):
        """
        Test order checkout if user is not authenticated and do not want to create profile.
        """
        self._add_product_into_cart()
        data = self._get_valid_form_data()
        response = self.client.post(self.url, data=data)
        self._test_order_checkout_redirect(response, reverse("shop:home"))
        self._test_message_about_receipt_send_email_is_displayed(
            list(get_messages(response.wsgi_request))[0].message
        )
        self.assertEqual(len(response.context["cart"]), 0)

    def test_order_checkout_if_user_is_not_authenticated_and_want_to_create_profile(
        self,
    ):
        """
        Test order checkout if user is not authenticated and want to create profile.
        """
        self._add_product_into_cart()
        response = self.client.post(
            self.url,
            data=self._get_valid_form_data(is_create_profile="True"),
        )
        messages = list(get_messages(response.wsgi_request))
        self._test_message_about_receipt_send_email_is_displayed(
            messages[0].message
        )
        self._test_user_successfully_created(messages)
        order = self._test_order_successfully_created(messages[3].message)
        self.assertEqual(len(response.context["cart"]), 0)
        self._test_order_checkout_redirect(
            response, reverse("order:detail", args=[order.id])
        )

    def test_order_checkout_if_user_is_authenticated(self):
        """Test order checkout if user is authenticated."""
        self._add_product_into_cart()
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            self.url,
            data={
                "phone_number": "+380123456789",
                "address": "Some address",
                "order_comment": "Some comment",
            },
        )
        messages = list(get_messages(response.wsgi_request))
        self._test_message_about_receipt_send_email_is_displayed(
            messages[0].message, email_prefix="test"
        )
        order = self._test_order_successfully_created(
            messages[1].message, username="testuser"
        )
        self.assertEqual(len(response.context["cart"]), 0)
        self._test_order_checkout_redirect(
            response, reverse("order:detail", args=[order.id])
        )

    def test_order_checkout_if_user_is_registered_and_want_to_create_profile(
        self,
    ):
        """
        Test order checkout if user is registered and want to create profile.
        """
        self._add_product_into_cart()
        response = self.client.post(
            self.url, data=self._get_valid_form_data(is_create_profile="True")
        )
        messages = list(get_messages(response.wsgi_request))
        self._test_message_about_receipt_send_email_is_displayed(
            messages[0].message
        )
        self._test_message_about_successfully_authentication(
            messages[1].message, username="john_doe"
        )
        order = self._test_order_successfully_created(messages[2].message)
        self.assertEqual(len(response.context["cart"]), 0)
        self._test_order_checkout_redirect(
            response, reverse("order:detail", args=[order.id])
        )

    def _add_product_into_cart(self):
        """Adds product into cart and checks that it was added successfully."""
        response = self.client.post(
            "/cart/add/",
            data=json.dumps({"product_id": self.product.id, "quantity": 1}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content.decode("utf-8"),
            "Product has successfully added to your cart.",
        )

    def _get_valid_form_data(
        self, is_create_profile: str = "False"
    ) -> dict[str, str]:
        """Returns valid form data with the given "is_create_profile" value."""
        data = {
            "is_create_profile": is_create_profile,
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+380123456789",
            "email": "user@example.com",
            "address": "Some address",
            "order_comment": "Some comment",
        }
        if is_create_profile == "True":
            data["username"] = "john_doe"
            data["password"] = "testpass"
        return data

    def _test_order_checkout_redirect(self, response: HttpResponse, url: str):
        """Test that order checkout redirects to the given url."""
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)

    def _test_message_about_receipt_send_email_is_displayed(
        self, message: str, email_prefix: str = "user"
    ):
        """Test that message about sending an email is displayed."""
        self.assertEqual(
            message,
            f"We've just sent a receipt email to {email_prefix}@example.com",
        )

    def _test_user_successfully_created(self, messages: list):
        """Test that user successfully created."""
        self.assertEqual(
            messages[1].message,
            f"Confirmation e-mail sent to user@example.com.",
        )
        self._test_message_about_successfully_authentication(
            messages[2].message, username="john_doe"
        )
        self.assertTrue(User.objects.filter(username="john_doe").exists())

    def _test_message_about_successfully_authentication(
        self, message: str, username: str
    ):
        """Test that message about successfully authentication is displayed."""
        self.assertEqual(message, f"Successfully signed in as {username}.")

    def _test_order_successfully_created(
        self, message: str, username: str = "john_doe"
    ) -> Order:
        """Test that order successfully created and returns it."""
        self.assertEqual(message, "Order has successfully created.")
        order = Order.objects.get(user__username=username)
        self.assertTrue(OrderItem.objects.filter(order_id=order.id).exists())
        return order


class OrderViewTestMixin(UserTestMixin):
    """Mixin for testing the "Order" app views."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Creates two users and an order for the first user."""
        super().setUpTestData()
        cls.order = Order.objects.create(user=cls.user, total_price=1500)
        cls.user2 = User.objects.create_user(
            username="testuser2", email="test2@test.com", password="testpass"
        )


class OrderListViewTestCase(
    ViewTestMixin, OrderViewTestMixin, LoginRequiredTestMixin, TestCase
):
    """Tests for the OrderListView."""

    url = "/order/list/"
    name = "order:list"
    is_login_required = True
    template_name = "order/order_list.html"

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        for _ in range(12):
            Order.objects.create(user=cls.user, total_price=1500)

    def test_order_list_page_message_with_empty_orders(self):
        """
        Test that the order list page with empty orders has correct message.
        """
        self.client.login(username="testuser2", password="testpass")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You don't have any orders yet.")

    def test_order_list_page_with_orders(self):
        """Test the order list page with orders."""
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, Order.objects.first().id)

    # * ------------------ Testing pagination functionality ------------------

    def test_pagination_is_ten(self):
        """Test that pagination is set to 10 per page."""
        self.assertEqual(len(self.response.context["page_obj"]), 10)

    def test_paginated_order_list(self):
        """Test that second page has (exactly) remaining 3 orders."""
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(f"{self.url}?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 3)


class OrderDetailViewTestCase(
    ViewTestMixin, OrderViewTestMixin, LoginRequiredTestMixin, TestCase
):
    """Tests for the OrderDetailView."""

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Sets kwargs and url attributes for the test class.
        Creates an order with 3 order items for the first user.
        """
        super().setUpTestData()
        cls.kwargs = {"pk": cls.order.id}
        cls.url = f"/order/{cls.order.id}/"

        brand = Brand.objects.create(name="Test brand")
        category = Category.objects.create(name="Test category")

        for count in range(1, 4):
            OrderItem.objects.create(
                order=cls.order,
                price=500,
                quantity=1,
                total_price=500,
                product=Product.objects.create(
                    name=f"Test product {count}",
                    description="Some content",
                    image=f"./some_image_{count}.jpg",
                    price=500,
                    year=2023,
                    brand=brand,
                    category=category,
                ),
            )

    name = "order:detail"
    is_login_required = True
    template_name = "order/order_detail.html"

    def test_404_with_not_user_order(self):
        """
        Test that the 404 page is returned if the user doesn't own the order.
        """
        self.client.login(username="testuser2", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_order_detail_page_contains_order_id(self):
        """Test that the order detail page contains the order id."""
        self.assertContains(self.response, self.order.id)

    def test_order_detail_page_contains_order_date(self):
        """Test that the order detail page contains the order date."""
        self.assertContains(self.response, f"Order date:")
        self.assertContains(
            self.response,
            datetime.now(pytz.timezone(settings.TIME_ZONE)).strftime(
                "%B %d, %Y, %H:%M"
            ),
        )

    def test_order_detail_page_contains_order_items(self):
        """Test that the order detail page contains the order items."""
        self.assertContains(self.response, f"Order items")
        self.assertContains(self.response, "Test product 1")
        self.assertContains(self.response, "Test product 2")
        self.assertContains(self.response, "Test product 3")

    def test_order_detail_page_contains_order_total_price(self):
        """Test that the order detail page contains the order total price."""
        self.assertContains(self.response, f"Order total price:")
        self.assertContains(self.response, f"{self.order.total_price}.0$")

    def test_order_detail_page_contains_remove_button(self):
        """Test that the order detail page contains the remove button."""
        self.assertContains(
            self.response, 'class="remove btn btn-danger btn-lg"'
        )


class OrderDeleteViewTestCase(
    OrderViewTestMixin, DeleteViewTestMixin, TestCase
):
    """Tests for the OrderDeleteView."""

    success_url = reverse_lazy("order:list")
    success_message = "Order has successfully deleted."

    @classmethod
    def setUpTestData(cls) -> None:
        """Sets the url attribute for the test class."""
        super().setUpTestData()
        cls.order_id = cls.order.id
        cls.url = f"/order/{cls.order.id}/delete/"

    def test_object_deleting(self):
        """Test that the order is deleted."""
        super().test_object_deleting()
        self.assertFalse(Order.objects.filter(id=self.order_id).exists())
