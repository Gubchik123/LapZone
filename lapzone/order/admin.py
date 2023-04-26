from django.urls import reverse
from django.contrib import admin
from django.utils.safestring import mark_safe, SafeText

from general.admin_mixins import (
    ModelWithPriceAdminMixin,
    ModelWithFKToProductAdminMixin,
    ModelWithFKToUserAdminMixin,
)
from .models import Order, OrderItem


@admin.register(Order)
class OrderModelAdmin(ModelWithFKToUserAdminMixin, admin.ModelAdmin):
    """Admin class for managing Order instances."""

    list_filter = ("user__username",)
    readonly_fields = ("get_user_link", "get_total_price", "created")
    list_display = ("id", "get_total_price", "get_user_link", "created")
    fields = (("user", "get_user_link"), "total_price", "created")

    def get_total_price(self, order: Order) -> str:
        """Returns string: total_price + '$'"""
        return f"{order.total_price} $"

    get_total_price.short_description = "Total price"


@admin.register(OrderItem)
class OrderItemModelAdmin(
    ModelWithPriceAdminMixin, ModelWithFKToProductAdminMixin, admin.ModelAdmin
):
    """Admin class for managing OrderItem instances."""

    list_display = (
        "id",
        "get_product_link",
        "get_price",
        "quantity",
        "get_order_link",
    )
    fields = (
        ("price", "quantity"),
        ("product", "get_product_link"),
        ("order", "get_order_link"),
    )
    search_fields = ("product__name",)
    search_help_text = "Searching by product"
    list_filter = ("order__id", "product__name")
    readonly_fields = ("get_product_link", "get_order_link")

    def get_order_link(self, order_item: OrderItem) -> SafeText:
        """Returns link to the admin page for order.order"""
        link_to_order = reverse(
            "admin:order_order_change", args=(order_item.order.pk,)
        )
        return mark_safe(
            f"<a href='{link_to_order}'>{order_item.order.id}</a>"
        )

    get_order_link.short_description = "For order"
