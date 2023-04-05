from django.test import TestCase

from general.test_mixins.for_views import ViewTestMixin
from shop.models import Brand, Category, Product, CarouselImage


class ShopAppViewsTestMixin(ViewTestMixin):
    """
    Test mixin providing helper methods for testing views in the "Shop" app.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Set up test data by creating 11 brands, 11 categories, and 11 products.
        """
        for count in range(11):
            brand = Brand.objects.create(name=f"Test brand {count}")
            category = Category.objects.create(name=f"Test category {count}")

            Product.objects.create(
                name=f"Test product {count}",
                description="Some content",
                image=f"./some_image_{count}.jpg",
                price=1000 + count,
                year=2023,
                brand=brand,
                category=category,
            )


class HomeViewTestCase(ShopAppViewsTestMixin, TestCase):
    """Tests for the HomeView."""

    url = "/"
    name = "shop:home"
    template_name = "shop/home.html"

    def test_lists_recently_added_products(self):
        """Test that recently added products are listed on the home page."""
        self.assertIn("recently_added_products", self.response.context)
        self.assertEqual(
            len(self.response.context["recently_added_products"]), 10
        )
        self.assertQuerysetEqual(
            self.response.context["recently_added_products"],
            Product.objects.order_by("-id")[:10],
        )

    def test_lists_brands(self):
        """Test that brands are listed on the home page."""
        self.assertIn("brands", self.response.context)
        self.assertQuerysetEqual(
            self.response.context["brands"], Brand.objects.all()
        )

    def test_lists_categories(self):
        """Test that categories are listed on the home page."""
        self.assertIn("categories", self.response.context)
        self.assertQuerysetEqual(
            self.response.context["categories"], Category.objects.all()
        )

    def test_lists_carousel_images(self):
        """Test that carousel images are listed on the home page."""
        self.assertIn("carousel_images", self.response.context)
        self.assertQuerysetEqual(
            self.response.context["carousel_images"],
            CarouselImage.objects.all(),
        )
