from decimal import Decimal

from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase

from shop.models import Product


class Cart:
    """
    Shopping cart that stores products, their quantities and their prices.
    """

    def __init__(self, request_session: SessionBase) -> None:
        """Initializes a new cart instance."""
        self.session = request_session
        if not (cart := self.session.get(settings.CART_SESSION_ID)):
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterates over the items in the cart and yield each item dictionary.
        """
        for product in Product.objects.filter(id__in=self.cart.keys()):
            self.cart[str(product.id)]["product"] = product

        for item in self.cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item
        # Remove not JSON serializable objects from the cart.
        for item in self.cart.values():
            del item["product"]
            item["price"] = str(item["price"])
            item["total_price"] = str(item["total_price"])

    def __len__(self) -> int:
        """
        Returns the total number of items in the cart based on their quantities.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def save(self) -> None:
        """Saves the current state of the cart to the session."""
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, product: Product, quantity: int) -> None:
        """Adds a product to the cart"""
        if (product_id := str(product.id)) not in self.cart:
            self.cart[product_id] = {
                "quantity": quantity,
                "price": str(product.price),
            }
            self.save()

    def update(self, product: Product, quantity: int) -> None:
        """Updates the cart product quantity."""
        if (product_id := str(product.id)) in self.cart:
            self.cart[product_id]["quantity"] = quantity
            self.save()

    def get_total_price(self) -> int:
        """Returns the total price of all items in the cart."""
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )

    def remove(self, product: Product) -> None:
        """Removes a product from the cart."""
        if (product_id := str(product.id)) in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self) -> None:
        """Clears all items from the cart."""
        self.cart.clear()
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
