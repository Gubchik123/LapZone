from uuid import uuid4

from django.test import TestCase

from shop import models as shop_models
from order.models import Order, OrderItem
from general.test_mixins.for_models import (
    ModelMetaOptionsTestMixin,
    ModelWithPriceTestMixin,
    ModelWithCreatedDateTimeTestMixin,
    ModelWithFKToProductTestMixin,
    ModelWithFKToUserTestMixin,
)


class OrderModelTestCase(
    ModelMetaOptionsTestMixin,
    ModelWithCreatedDateTimeTestMixin,
    ModelWithFKToUserTestMixin,
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

    def test_id_unique(self):
        """Test that the id field is unique."""
        self.assertTrue(self.model._meta.get_field("id").unique)

    def test_id_editable(self):
        """Test that the id field is not editable."""
        self.assertFalse(self.model._meta.get_field("id").editable)

    def test_id_primary_key(self):
        """Test that the id field is the primary key."""
        self.assertTrue(self.model._meta.get_field("id").primary_key)

    def test_id_verbose_name(self):
        """Test that the id field's verbose name is "ID"."""
        self.assertEqual(self.model._meta.get_field("id").verbose_name, "ID")

    def test_id_default(self):
        """Test that the id field has default value of uuid4."""
        self.assertEqual(self.model._meta.get_field("id").default, uuid4)

    def test_total_price_blank(self):
        """Test that the total_price field is not blank."""
        self.assertFalse(self.model._meta.get_field("total_price").blank)

    def test_total_price_verbose_name(self):
        """Test that the total_price field's verbose name is "Total price"."""
        self.assertEqual(
            self.model._meta.get_field("total_price").verbose_name,
            "Total price",
        )


class OrderItemModelTestCase(
    ModelMetaOptionsTestMixin,
    ModelWithPriceTestMixin,
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
        cls.order = Order.objects.create(
            user=shop_models.User.objects.create(
                username="Someone", email="test@test.com", password="123"
            ),
            total_price=1000,
        )
        cls.order_item = OrderItem.objects.create(
            order=cls.order,
            product=shop_models.Product.objects.create(
                name="Test laptop",
                description="Some content",
                image="./some_image.jpg",
                price=1000,
                year=2023,
                brand=shop_models.Brand.objects.create(name="test brand"),
                category=shop_models.Category.objects.create(
                    name="test category"
                ),
            ),
            price=1000,
            quantity=1,
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
