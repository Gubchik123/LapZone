from decimal import Decimal

from django.conf import settings
from django.http import HttpRequest

from shop.models import Product


class Cart:
    """
    Shopping cart that stores products, their quantities and their prices.
    """

    def __init__(self, request: HttpRequest) -> None:
        """Initializes a new cart instance."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
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

    def __len__(self) -> int:
        """
        Returns the total number of items in the cart based on their quantities.
        """
        return sum(item_dict["quantity"] for item_dict in self.cart.values())

    def save(self) -> None:
        """Saves the current state of the cart to the session."""
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(
        self,
        product: Product,
        quantity: int = 1,
        update_quantity: bool = False,
    ) -> None:
        """Adds a product to the cart or updates its quantity."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
            }
        if update_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def get_total_price(self) -> int:
        """Returns the total price of all items in the cart."""
        return sum(
            Decimal(item_dict["price"]) * item_dict["quantity"]
            for item_dict in self.cart.values()
        )

    def remove(self, product: Product) -> None:
        """Removes a product from the cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self) -> None:
        """Clears all items from the cart."""
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
