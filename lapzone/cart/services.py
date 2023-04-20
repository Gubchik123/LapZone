import json
import logging

from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from shop.models import Product
from .cart import Cart


logger = logging.getLogger(__name__)


def _get_product_id_from_(json_data: dict, prefix: str) -> int | str:
    """Extracts product ID from json and returns it or error message."""
    product_id: int | None = None
    try:
        product_id = int(json_data["product_id"])
        return product_id
    except (KeyError, ValueError, TypeError):
        logger.error(f"cart product {prefix}: product_id={product_id}")
        return "There was an error! Try again later."


def add_product_to_cart_and_get_response_message(request: HttpRequest) -> str:
    """Adds a product to cart and returns a response message."""
    json_data: dict = json.loads(request.body)
    product_id = _get_product_id_from_(json_data, prefix="adding")
    if isinstance(product_id, str):
        return product_id  # Error message.

    Cart(request).add(
        get_object_or_404(Product, id=product_id), json_data.get("quantity", 1)
    )
    return "Product has successfully added to your cart."


def remove_product_from_cart(request: HttpRequest) -> str:
    """Removes a product from cart and adds a response message in messages."""
    product_id = _get_product_id_from_(
        json.loads(request.body), prefix="removing"
    )
    if isinstance(product_id, str):
        messages.error(request, product_id)  # Error message

    Cart(request).remove(get_object_or_404(Product, id=product_id))
    messages.success(
        request, "Product has successfully removed from your cart."
    )
