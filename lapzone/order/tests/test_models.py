from django.test import TestCase

from shop import models as shop_models
from order.models import Order, OrderItem
from general.test_mixins.for_views import ProductTestMixin
from general.test_mixins.for_models import (
    ModelMetaOptionsTestMixin,
    ModelWithUUIDPKTestMixin,
    ModelWithPriceTestMixin,
    ModelWithCreatedDateTimeTestMixin,
    ModelWithFKToProductTestMixin,
    ModelWithFKToUserTestMixin,
)


class ModelWithTotalPriceTestMixin:
    """Mixin for testing the 'total_price' field parameters
    for models that inherited from abstract ModelWithTotalPrice."""

    def test_total_price_blank(self):
        """Test that the total_price field is not blank."""
        self.assertFalse(self.model._meta.get_field("total_price").blank)

    def test_total_price_verbose_name(self):
        """Test that the total_price field's verbose name is "Total price"."""
        self.assertEqual(
            self.model._meta.get_field("total_price").verbose_name,
            "Total price",
        )


class OrderModelTestCase(
    ModelMetaOptionsTestMixin,
    ModelWithUUIDPKTestMixin,
    ModelWithCreatedDateTimeTestMixin,
    ModelWithFKToUserTestMixin,
    ModelWithTotalPriceTestMixin,
    TestCase,
):
    """Tests for the Order model."""

    model = Order
    verbose_name = "Order"
    verbose_name_plural = "Orders"
    ordering = ["-created", "-total_price"]

    @classmethod
    def setUpTestData(cls) -> None:
        """Creates the first Order for testing."""
        cls.order = Order.objects.create(
            user=shop_models.User.objects.create(
                username="Someone", email="test@test.com", password="123"
            ),
            total_price=1000,
        )

    def test_model_string_representation(self):
        """Test the model string representation by __str__."""
        self.assertEqual(
            str(self.order), f"Order {self.order.id} from {self.order.user}"
        )

    def test_get_absolute_url(self):
        """Test the get_absolute_url method."""
        self.assertEqual(
            self.order.get_absolute_url(), f"/order/{self.order.id}/"
        )


class OrderItemModelTestCase(
    ProductTestMixin,
    ModelMetaOptionsTestMixin,
    ModelWithPriceTestMixin,
    ModelWithTotalPriceTestMixin,
    ModelWithFKToProductTestMixin,
    TestCase,
):
    """Tests for the OrderItem model."""

    model = OrderItem
    verbose_name = "Order item"
    verbose_name_plural = "Order items"
    ordering = ["order_id", "product_id"]

    @classmethod
    def setUpTestData(cls) -> None:
        """Creates the first OrderItem for testing."""
        super().setUpTestData()
        cls.order = Order.objects.create(
            user=shop_models.User.objects.create(
                username="Someone", email="test@test.com", password="123"
            ),
            total_price=1000,
        )
        cls.order_item = OrderItem.objects.create(
            order=cls.order,
            product=cls.product,
            price=1000,
            quantity=1,
            total_price=1000,
        )

    def test_model_string_representation(self):
        """Test the model string representation by __str__."""
        self.assertEqual(
            str(self.order_item),
            f"{self.order_item.quantity}x {self.order_item.product} for {self.order_item.order_id}",
        )

    def test_quantity_blank(self):
        """Test that the quantity field is not blank."""
        self.assertFalse(self.model._meta.get_field("quantity").blank)

    def test_quantity_verbose_name(self):
        """Test that the quantity field's verbose name is "Quantity"."""
        self.assertEqual(
            self.model._meta.get_field("quantity").verbose_name, "Quantity"
        )

    def test_order_related_model(self):
        """Test that the order field is related to the Order model."""
        self.assertEqual(
            self.model._meta.get_field("order").related_model, Order
        )

    def test_order_verbose_name(self):
        """Test that the order field's verbose name is "Order"."""
        self.assertEqual(
            self.model._meta.get_field("order").verbose_name, "Order"
        )

    def test_order_on_delete_cascade(self):
        """Test that the order field's on_delete is CASCADE."""
        self.order.delete()
        with self.assertRaises(OrderItem.DoesNotExist):
            OrderItem.objects.get(id=1)
