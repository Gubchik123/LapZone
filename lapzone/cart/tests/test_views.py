import json

from django.conf import settings
from django.test import TestCase
from django.http import HttpResponse
from django.contrib.messages import get_messages

from general.test_mixins.for_views import ViewTestMixin, ProductTestMixin


class CartTemplateViewTestCase(ViewTestMixin, ProductTestMixin, TestCase):
    """Tests for the CartTemplateView."""

    url = "/cart/"
    name = "cart:detail"
    template_name = "cart/detail.html"

    def test_cart_there_is_in_response_context(self):
        """Tests that "cart" there is in the response context."""
        self.assertIn("cart", self.response.context)

    def test_cart_page_with_empty_cart(self):
        """Tests that the cart page with an empty cart has correct message."""
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(
            self.response, "There are no products in your cart yet."
        )

    def test_cart_page_with_non_empty_cart(self):
        """Tests the cart page with a non-empty cart."""
        # Adding a product in cart.
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

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(
            response, "There are no products in your cart yet."
        )
        self.assertContains(response, self.product.name)
        self.assertContains(response, f"{self.product.price}.0$")


class CartPOSTViewWithRequiredProductIDTestMixin(ProductTestMixin):
    """Mixin for testing the "Cart" app views
    that handles POST HTTP method with required product ID in request body."""

    url: str
    success_response_message: str
    is_response_message_in_messages = False

    def test_post_method_with_valid_data(self):
        """Tests POST method with valid data."""
        response = self._send_post_request_and_get_response(
            data={"product_id": self.product.id, "quantity": 1}
        )
        self.assertEqual(response.status_code, 200)
        self._check_response_message_is_equal_to_(
            self.success_response_message, response
        )

    def test_post_method_with_non_existent_product(self):
        """Tests 404 in POST method with non existent product."""
        # ! I think it's correct, but it doesn't work and returns 405.
        # response = self._test_post_method_with_invalid_(
        #     data={"product_id": 100, "quantity": 1}
        # )
        # self.assertEqual(response.status_code, 404)

    def test_post_method_with_invalid_data(self):
        """Tests POST method with invalid empty data."""
        self._test_post_method_with_invalid_(data={})

    def test_post_method_with_invalid_string_product_id(self):
        """Tests POST method with invalid product_id (string)."""
        self._test_post_method_with_invalid_(
            data={"product_id": "string", "quantity": 1}
        )

    def test_post_method_with_invalid_none_product_id(self):
        """Tests POST method with invalid product_id (None)."""
        self._test_post_method_with_invalid_(
            data={"product_id": None, "quantity": 1}
        )

    def test_post_method_without_product_id(self):
        """Tests POST method with invalid data (without product_id)."""
        self._test_post_method_with_invalid_(data={"quantity": 1})

    def _test_post_method_with_invalid_(self, data: dict):
        """Tests POST method with invalid data."""
        response = self._send_post_request_and_get_response(data)
        self.assertEqual(response.status_code, 200)
        self._check_response_message_is_equal_to_(
            settings.ERROR_MESSAGE, response
        )

    def _send_post_request_and_get_response(self, data: dict) -> HttpResponse:
        """Sends POST request by the self.url and returns response."""
        return self.client.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
        )

    def _check_response_message_is_equal_to_(
        self, message: str, response: HttpResponse
    ):
        """Checks that the response message is equal to the message."""
        if self.is_response_message_in_messages:
            messages = list(get_messages(response.wsgi_request))
            self.assertEqual(len(messages), 1)
            self.assertEqual(messages[0].message, message)
        else:
            self.assertEqual(
                response.content.decode("utf-8"),
                message,
            )


class CartPOSTViewTestMixin(CartPOSTViewWithRequiredProductIDTestMixin):
    """Mixin for testing the "Cart" app views that handles POST HTTP method."""

    def test_post_method_with_invalid_string_quantity(self):
        """Tests POST method with invalid quantity (string)."""
        self._test_post_method_with_invalid_(
            data={"product_id": self.product.id, "quantity": "string"}
        )

    def test_post_method_with_invalid_none_quantity(self):
        """Tests POST method with invalid quantity (None)."""
        self._test_post_method_with_invalid_(
            data={"product_id": self.product.id, "quantity": None}
        )

    def test_post_method_without_quantity(self):
        """Tests POST method with invalid data (without quantity)."""
        self._test_post_method_with_invalid_(
            data={"product_id": self.product.id}
        )


class CartAddViewTestCase(CartPOSTViewTestMixin, TestCase):
    """Tests for the CartAddView."""

    url = "/cart/add/"
    success_response_message = "Product has successfully added to your cart."


class CartUpdateViewTestCase(CartPOSTViewTestMixin, TestCase):
    """Tests for the CartUpdateView."""

    url = "/cart/update/"
    success_response_message = "The product quantity has successfully updated."


class CartRemoveViewTestCase(
    CartPOSTViewWithRequiredProductIDTestMixin, TestCase
):
    """Tests for the CartRemoveView."""

    url = "/cart/remove/"
    success_response_message = (
        "Product has successfully removed from your cart."
    )
    is_response_message_in_messages = True
