import uuid

from django.db import models

from general.models import (
    ModelWithPrice,
    ModelWithCreatedDateTime,
    ModelWithFKToProduct,
    ModelWithFKToUser,
)


class Order(ModelWithFKToUser, ModelWithCreatedDateTime, models.Model):
    """
    A model representing a user order.
    Fields: id (uuid4), user, created, total_price.
    """

    id = models.UUIDField(
        unique=True,
        editable=False,
        primary_key=True,
        verbose_name="ID",
        default=uuid.uuid4,
    )
    total_price = models.FloatField(blank=False, verbose_name="Total price")

    def __str__(self) -> str:
        """Returns string representation of the Order model."""
        return f"Order {self.id} from {self.user}"

    class Meta:
        """Meta options for the Order model."""

        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created", "-total_price"]


class OrderItem(ModelWithFKToProduct, ModelWithPrice, models.Model):
    """
    A model representing an item in the order.
    Fields: product, price, quantity, order.
    """

    quantity = models.PositiveIntegerField(
        blank=False, verbose_name="Quantity"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name="Order"
    )

    def __str__(self) -> str:
        """Returns string representation of the OrderItem model."""
        return f"{self.quantity}x {self.product} for {self.order_id}"

    class Meta:
        """Meta options for the OrderItem model."""

        verbose_name = "Order item"
        verbose_name_plural = "Order items"
        ordering = ["order_id", "product_id"]
