from django.http import HttpRequest

from .cart import Cart 


def cart(request: HttpRequest) -> dict[str, Cart]:
    """Returns a dictionary with the cart object."""
    return {"cart": Cart(request)}
