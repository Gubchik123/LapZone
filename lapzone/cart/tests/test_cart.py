from decimal import Decimal

from django.conf import settings
from django.test import TestCase
from django.contrib.sessions.backends.db import SessionStore

from shop.models import Brand, Category, Product
from cart.cart import Cart


class CartTestCase(TestCase):
    """Tests for the 'Cart' class."""

    def setUp(self):
        """Initializes a new cart instance and a product instance."""
        self.product = Product.objects.create(
            name=f"Test product",
            description="Some content",
            image=f"./some_image.jpg",
            price=Decimal("10.00"),
            year=2023,
            brand=Brand.objects.create(name="Test brand"),
            category=Category.objects.create(name="Test category"),
        )
        self.session = SessionStore()
        self.cart = Cart(self.session)

    def test_iter(self):
        """Tests iteration over items in the cart (__iter__)."""
        self.cart.add(self.product, quantity=2)

        items = list(self.cart)
        self.assertEqual(len(items), 1)

        item = items[0]
        self.assertEqual(item["product"], self.product)
        self.assertEqual(item["quantity"], 2)
        self.assertEqual(item["price"], Decimal("10.00"))
        self.assertEqual(item["total_price"], Decimal("20.00"))

    def test_len(self):
        """Tests getting the total number of items in the cart (__len__)."""
        self.cart.add(self.product, quantity=2)
        self.assertEqual(len(self.cart), 2)

    def test_saving(self):
        """Tests saving the cart to the session."""
        self.cart.add(self.product, quantity=1)
        self.cart.save()
        self.assertEqual(
            self.session.get(settings.CART_SESSION_ID), self.cart.cart
        )

    def test_adding(self):
        """Tests adding a product to the cart."""
        self.cart.add(self.product, quantity=1)
        self.assertEqual(len(self.cart), 1)
        self.assertEqual(self.cart.get_total_price(), Decimal("10.00"))

    def test_updating(self):
        """Tests updating a product in the cart."""
        self.cart.add(self.product, quantity=1)
        self.assertEqual(len(self.cart), 1)
        self.assertEqual(self.cart.get_total_price(), Decimal("10.00"))

        self.cart.update(self.product, quantity=2)
        self.assertEqual(len(self.cart), 2)
        self.assertEqual(self.cart.get_total_price(), Decimal("20.00"))

    def test_removing(self):
        """Tests removing a product from the cart."""
        self.cart.add(self.product, quantity=1)
        self.cart.remove(self.product)
        self.assertEqual(len(self.cart), 0)
        self.assertEqual(self.cart.get_total_price(), Decimal("0.00"))
