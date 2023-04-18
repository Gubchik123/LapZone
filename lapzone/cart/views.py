from typing import Any

from django.views import generic
from django.http import HttpRequest, HttpResponse

from general.views import BaseView
from .cart import Cart
from . import services


class CartDetailView(BaseView, generic.TemplateView):
    """View for displaying the contents of the user's shopping cart."""

    template_name = "cart/detail.html"


class CartAddView(BaseView, generic.View):
    """View for adding a product to the user's cart via POST request."""

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Returns response message from service adding function."""
        return HttpResponse(
            services.add_product_to_cart_and_get_response_message(request)
        )


class CartRemoveView(BaseView, generic.View):
    """View for removing a product from the user's cart via POST request."""

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Returns response message from service removing function."""
        return HttpResponse(
            services.remove_product_from_cart_and_get_response_message(request)
        )
