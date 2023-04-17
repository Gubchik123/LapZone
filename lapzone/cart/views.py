from typing import Any

from django.views import generic

from general.views import BaseView
from .cart import Cart


class CartDetailView(BaseView, generic.TemplateView):
    """View for displaying the contents of the user's shopping cart."""

    template_name = "cart/detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Adds the user's cart to the template context data and returns it."""
        context = super().get_context_data(**kwargs)
        context["cart"] = Cart(self.request)
        return context
