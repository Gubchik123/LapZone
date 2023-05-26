from django.urls import reverse
from django.db.models import Model
from django.utils.safestring import mark_safe, SafeText


class ModelWithPriceAdminMixin:
    """Admin mixin for managing instances that
    inherited form abstract ModelWithPrice."""

    def get_price(self, model: Model) -> str:
        """Returns string: price + '$'"""
        return f"{model.price} $"

    get_price.short_description = "Price"


class ModelWithFKToProductAdminMixin:
    """Admin mixin for managing instances that
    inherited form abstract ModelWithFKToProduct."""

    list_filter = ("product",)

    def get_product_link(self, model: Model) -> SafeText | str:
        """Returns link to the admin page for shot product."""
        if model.product:
            link_to_product = reverse(
                "admin:shop_product_change", args=(model.product.pk,)
            )
            return mark_safe(
                f"<a href='{link_to_product}'>{model.product.name}</a>"
            )
        return "None"

    get_product_link.short_description = "Product"


class ModelWithFKToUserAdminMixin:
    """Admin mixin for managing instances that
    inherited form abstract ModelWithFKToUser."""

    def get_user_link(self, model: Model) -> SafeText:
        """Returns link to the admin page for user like."""
        link_to_user = reverse("admin:auth_user_change", args=(model.user.pk,))
        return mark_safe(f"<a href='{link_to_user}'>{model.user.username}</a>")

    get_user_link.short_description = "User"
