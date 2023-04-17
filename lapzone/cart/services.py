import json
import logging

from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from shop.models import Product
from .cart import Cart


logger = logging.getLogger(__name__)


def _get_product_id_from_(request_body: bytes, prefix: str) -> int | str:
    """
    Extracts product ID from request body and returns it or error message.
    """
    data = json.loads(request_body)
    try:
        product_id = int(data["product_id"])
        return product_id
    except (KeyError, ValueError, TypeError):
        logger.error(f"cart product {prefix}: product_id={product_id}")
        return "There was an error! Try again later."


def add_product_to_cart_and_get_response_message(request: HttpRequest) -> str:
    """Adds a product to cart and returns a response message."""
    product_id = _get_product_id_from_(request.body, prefix="adding")
    if isinstance(product_id, str):
        return product_id  # Error message.

    Cart(request).add(get_object_or_404(Product, id=product_id))
    return "Product has successfully added to your cart."
