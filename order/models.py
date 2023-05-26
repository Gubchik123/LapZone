from django.db import models
from django.urls import reverse

from general.models import (
    ModelWithUUIDPK,
    ModelWithPrice,
    ModelWithCreatedDateTime,
    ModelWithFKToProduct,
    ModelWithFKToUser,
)


class ModelWithTotalPrice(models.Model):
    """Abstract model with 'total_price' FloatField."""

    total_price = models.FloatField(blank=False, verbose_name="Total price")

    class Meta:
        abstract = True


class Order(
    ModelWithUUIDPK,
    ModelWithFKToUser,
    ModelWithCreatedDateTime,
    ModelWithTotalPrice,
    models.Model,
):
    """
    A model representing a user order.
    Fields: id (uuid4), user, created, total_price.
    """

    def __str__(self) -> str:
        """Returns string representation of the Order model."""
        return f"Order {self.id} from {self.user}"

    def get_absolute_url(self) -> str:
        """Returns the URL to the order detail page."""
        return reverse("order:detail", kwargs={"pk": self.pk})

    class Meta:
        """Meta options for the Order model."""

        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created", "-total_price"]


class OrderItem(
    ModelWithFKToProduct, ModelWithPrice, ModelWithTotalPrice, models.Model
):
    """
    A model representing an item in the order.
    Fields: product, price, total_price, quantity, order.
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
