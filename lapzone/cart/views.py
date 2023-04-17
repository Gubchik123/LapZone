from typing import Any

from django.views import generic
from django.http import HttpRequest, HttpResponse

from general.views import BaseView
from .cart import Cart
from . import services


class CartDetailView(BaseView, generic.TemplateView):
    """View for displaying the contents of the user's shopping cart."""

    template_name = "cart/detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Adds the user's cart to the template context data and returns it."""
        context = super().get_context_data(**kwargs)
        context["cart"] = Cart(self.request)
        return context


class CartAddView(BaseView, generic.View):
    """View for adding a product to the user's cart via POST request."""

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Returns response message from service adding function."""
        return HttpResponse(
            services.add_product_to_cart_and_get_response_message(request)
        )
