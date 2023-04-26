from django.urls import reverse
from django.db.models import Model
from django.utils.safestring import mark_safe, SafeText


class ModelWithFKToProductAdminMixin:
    """Admin mixin for managing instances that
    inherited form abstract ModelWithFKToProduct"""

    list_filter = ("product",)

    def get_product_link(self, model: Model) -> SafeText:
        """Returns link to the admin page for shot.product"""
        link_to_product = reverse(
            "admin:shop_product_change", args=(model.product.pk,)
        )
        return mark_safe(
            f"<a href='{link_to_product}'>{model.product.name}</a>"
        )

    get_product_link.short_description = "Product"
