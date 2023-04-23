import json
import logging

from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from shop.models import Product
from .cart import Cart


logger = logging.getLogger(__name__)


def _get_product_id_and_quantity_from_(
    json_data: dict, prefix: str
) -> tuple[int, int] | str:
    """
    Extracts product ID and quantity from json and returns it or error message.
    """
    product_id = quantity = None
    try:
        product_id = int(json_data["product_id"])
        quantity = int(json_data["quantity"])
        return (product_id, quantity)
    except (KeyError, ValueError, TypeError):
        logger.error(f"cart product {prefix}: {product_id=}, {quantity=}")
        return ("There was an error! Try again later.", None)


def _process_cart_product(request: HttpRequest, action: str) -> str:
    """
    Processes a cart product based on action and returns a response message.
    """
    product_id, quantity = _get_product_id_and_quantity_from_(
        json.loads(request.body), prefix=action
    )
    if isinstance(product_id, str):
        return product_id  # Error message.

    product = get_object_or_404(Product, id=product_id)
    if action == "adding":
        Cart(request.session).add(product, quantity)
        return "Product has successfully added to your cart."

    Cart(request.session).update(product, quantity)
    return "The product quantity has successfully updated."


def add_product_to_cart_and_get_response_message(request: HttpRequest) -> str:
    """Adds a product to cart and returns a response message."""
    return _process_cart_product(request, action="adding")


def update_cart_product_and_get_response_message(request: HttpRequest) -> str:
    """Updates a cart product and returns a response message."""
    return _process_cart_product(request, action="updating")


def remove_product_from_cart(request: HttpRequest) -> None:
    """Removes a product from cart and adds a response message in messages."""
    product_id = json.loads(request.body).get(
        "product_id", "There was an error! Try again later."
    )
    if isinstance(product_id, str):
        messages.error(request, product_id)  # Error message
        return
    Cart(request.session).remove(get_object_or_404(Product, id=product_id))
    messages.success(
        request, "Product has successfully removed from your cart."
    )
