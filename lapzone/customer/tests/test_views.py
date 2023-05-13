from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.contrib.messages import get_messages
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.validators import UnicodeUsernameValidator

from customer.forms import UserModelForm
from shop.models import Brand, Category, Product, Like
from general.test_mixins.for_views import (
    ViewTestMixin,
    LoginRequiredTestMixin,
    DeleteViewTestMixin,
)


class CustomerViewTestMixin:
    """Test mixin for the "Customer" app views."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Creates a user for the tests."""
        cls.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass"
        )


class CustomerDetailViewTestCase(
    ViewTestMixin, LoginRequiredTestMixin, CustomerViewTestMixin, TestCase
):
    """Tests for the CustomerDetailView."""

    url = "/profile/"
    name = "customer:detail"
    template_name = "customer/detail.html"
    is_login_required = True

    def test_form_is_on_page(self):
        """Test that the UserModelForm there is on a page."""
        self.assertIn("form", self.response.context)
        self.assertIsInstance(self.response.context["form"], UserModelForm)

    def test_form_initial_user_data(self):
        """Test that the UserModelForm contains the initial user data."""
        form = self.response.context["form"]
        self.assertEqual(form.initial["username"], self.user.username)
        self.assertEqual(form.initial["first_name"], "")
        self.assertEqual(form.initial["last_name"], "")

    def test_date_joined_is_on_page(self):
        """Test that the date joined is on the page."""
        self.assertContains(self.response, "Date joined:")
        self.assertContains(
            self.response, self.user.date_joined.strftime("%B %d, %Y")
        )

    def test_change_password_link_is_on_page(self):
        """Test that the change password link is on the page."""
        self.assertContains(self.response, reverse("account_change_password"))

    def test_wish_list_link_is_on_page(self):
        """Test that the wish list link is on the page."""
        self.assertContains(self.response, reverse("customer:wish_list"))

    def test_order_list_link_is_on_page(self):
        """Test that the order list link is on the page."""
        self.assertContains(self.response, reverse("order:list"))

    def test_email_addresses_link_is_on_page(self):
        """Test that the email addresses link is on the page."""
        self.assertContains(self.response, reverse("account_email"))

    def test_social_account_connections_link_is_on_page(self):
        """Test that the social account connections link is on the page."""
        self.assertContains(
            self.response, reverse("socialaccount_connections")
        )

    def test_logout_link_is_on_page(self):
        """Test that the logout link is on the page."""
        self.assertContains(self.response, reverse("account_logout"))

    def test_delete_account_button_is_on_page(self):
        """Test that the delete account button is on the page."""
        self.assertContains(self.response, "Danger zone")
        self.assertContains(self.response, reverse("customer:delete"))
        self.assertContains(self.response, "Delete my account")


class CustomerWishListViewTestCase(
    ViewTestMixin, LoginRequiredTestMixin, CustomerViewTestMixin, TestCase
):
    """Tests for the CustomerWishListView."""

    url = "/profile/wish-list/"
    name = "customer:wish_list"
    template_name = "customer/wish_list.html"
    is_login_required = True

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

        brand = Brand.objects.create(name="test brand")
        category = Category.objects.create(name="test category")

        for count in range(1, 16):
            Like.objects.create(
                user=cls.user,
                product=Product.objects.create(
                    name=f"Test laptop {count}",
                    description="Some content",
                    image=f"./some_image_{count}.jpg",
                    price=1000,
                    year=2023,
                    brand=brand,
                    category=category,
                ),
            )

    def test_wish_list_page_alert_with_empty_wish_list(self):
        """Test that the alert is on the page if the wish list is empty."""
        User.objects.create_user(
            username="testuser2", email="test2@test.com", password="testpass"
        )
        self.client.login(username="testuser2", password="testpass")
        response = self.client.get(self.url)
        self.assertContains(response, "Your wish list is empty yet.")

    def test_wish_list_page_alert_with_non_empty_wish_list(self):
        """Test that 15th and 4th liked product is on the page."""
        self.assertContains(self.response, "Test laptop 13")
        self.assertContains(self.response, "Test laptop 4")

    # * ------------------ Testing pagination functionality ------------------

    def test_pagination_is_twelve(self):
        """Test that pagination is set to 12 per page."""
        self.assertEqual(len(self.response.context["page_obj"]), 12)

    def test_paginated_wish_list(self):
        """Test that second page has (exactly) remaining 3 liked products."""
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(f"{self.url}?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 3)


class CustomerUpdateViewTestCase(CustomerViewTestMixin, TestCase):
    """Tests for the CustomerUpdateView."""

    url = "/profile/update/"
    success_url = "/profile/"

    def test_form_valid(self):
        """Test that the user data is updated."""
        self.assertTrue(UserModelForm(self._get_valid_form_data()).is_valid())

    def test_user_has_updated(self):
        """Test that the user data has successfully updated."""
        data = self._get_valid_form_data()
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(self.url, data, follow=True)

        user = User.objects.get(username=data["username"])
        self.assertEqual(user.first_name, data["first_name"])
        self.assertEqual(user.last_name, data["last_name"])

        self.assertEqual(response.status_code, 200)
        self._test_response_message(
            response.wsgi_request,
            "Your personal data has successfully updated.",
        )

    def test_valid_redirect(self):
        """
        Test that the user is redirected to the success url if the form is valid.
        """
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(self.url, self._get_valid_form_data())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.success_url)

    def test_form_invalid(self):
        """Test that the form is invalid if the username is invalid."""
        data = self._get_valid_form_data(username="Invalid username")
        self.assertFalse(UserModelForm(data).is_valid())

    def test_user_has_not_updated(self):
        """Test that the user data has not successfully updated."""
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            self.url,
            self._get_valid_form_data(username="Invalid username"),
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.url, self.success_url)
        self._test_response_message(
            response.wsgi_request, UnicodeUsernameValidator.message
        )

    def test_invalid_redirect(self):
        """
        Test that the user is redirected to the success url if the form is not valid.
        """
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            self.url, self._get_valid_form_data(username="Invalid username")
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.success_url)

    def _get_valid_form_data(self, username="test_username") -> dict[str, str]:
        """Return valid form data."""
        return {
            "username": username,
            "first_name": "Test",
            "last_name": "User",
        }

    def _test_response_message(self, wsgi_request: WSGIRequest, message: str):
        """Test that the message is displayed."""
        messages = list(get_messages(wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, message)


class CustomerDeleteViewTestCase(
    CustomerViewTestMixin, DeleteViewTestMixin, TestCase
):
    """Tests for the CustomerDeleteView."""

    url = "/profile/delete/"
    success_url = reverse_lazy("shop:home")
    success_message = "Profile has successfully deleted."

    def test_object_deleting(self):
        """Test that the user is deleted."""
        super().test_object_deleting()
        self.assertFalse(User.objects.filter(username="testuser").exists())
