from django.views import generic
from django.http import HttpRequest, HttpResponse

from general.views import BaseView
from . import services


class CartAddView(BaseView, generic.View):
    """View for adding a product to the user's cart via POST request."""

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Returns response message from service adding function."""
        return HttpResponse(
            services.add_product_to_cart_and_get_response_message(request)
        )


class CartUpdateView(BaseView, generic.View):
    """View for updating a product in the user's cart via POST request."""

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Returns response message from service updating function."""
        return HttpResponse(
            services.update_cart_product_and_get_response_message(request)
        )


class CartRemoveView(BaseView, generic.View):
    """View for removing a product from the user's cart via POST request."""

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Returns response message from service removing function."""
        services.remove_product_from_cart(request)
        return HttpResponse(status=200)
