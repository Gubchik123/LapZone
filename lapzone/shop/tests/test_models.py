from typing import NoReturn

from django.contrib.auth.models import User
from django.test import TestCase, SimpleTestCase

from general.test_mixins import (
    ModelMetaOptionsTestMixin,
    ModelWithNameTestMixin,
    ModelWithNameAndSlugTestMixin,
    ModelWithDescriptionTestMixin,
    ModelWithImageTestMixin,
    ModelWithCreatedDateTimeTestMixin,
    ModelWithFKToProductTestMixin,
)
from shop.models import Brand, Category, Product, ProductShot, Like, Review


class BrandModelTest(
    ModelMetaOptionsTestMixin, ModelWithNameAndSlugTestMixin, TestCase
):
    """Test cases for the Brand model."""

    model = Brand
    ordering = ["name"]
    verbose_name = "Brand"
    verbose_name_plural = "Brands"
    # Redefined default parameter values of the abstract model(s).
    name_max_length = 30
    slug_max_length = 30

    expected_slug = "test-brand"

    @classmethod
    def setUpTestData(cls) -> NoReturn:
        """Creates the first Brand for testing."""
        Brand.objects.create(name="test brand")


class CategoryModelTest(
    ModelMetaOptionsTestMixin, ModelWithNameAndSlugTestMixin, TestCase
):
    """Test cases for the Category model."""

    model = Category
    ordering = ["name"]
    verbose_name = "Category"
    verbose_name_plural = "Categories"
    # Redefined default parameter values of the abstract model(s).
    name_max_length = 50
    slug_max_length = 50

    expected_slug = "test-category"

    @classmethod
    def setUpTestData(cls) -> NoReturn:
        """Creates the first Category for testing."""
        Category.objects.create(name="test category")


class ModelWithDescriptionAndImageTestMixin(
    ModelWithDescriptionTestMixin, ModelWithImageTestMixin
):
    """
    Mixin for both ModelWithDescriptionTestMixin and ModelWithImageTestMixin
    """


class ProductModelTest(
    ModelMetaOptionsTestMixin,
    ModelWithNameAndSlugTestMixin,
    ModelWithDescriptionAndImageTestMixin,
    TestCase,
):
    """Test cases for the Product model."""

    model = Product
    verbose_name = "Product"
    verbose_name_plural = "Products"
    ordering = ["name", "-price"]
    # Redefined default parameter values of the abstract model(s).
    image_upload_to = "products/"

    expected_slug = "test-laptop"

    @classmethod
    def setUpTestData(cls) -> NoReturn:
        """Creates the first Product for testing."""
        Product.objects.create(
            name="Test laptop",
            description="Some content",
            image="./some_image.jpg",
            price=1000,
            year=2023,
            brand=Brand.objects.create(name="test brand"),
            category=Category.objects.create(name="test category"),
        )

    def test_price_verbose_name(self):
        """Test that the price field's verbose name is "Price"."""
        self.assertEqual(
            self.model._meta.get_field("price").verbose_name, "Price"
        )

    def test_price_blank(self):
        """Test that the price field's blank is False."""
        self.assertEqual(self.model._meta.get_field("price").blank, False)

    def test_year_verbose_name(self):
        """Test that the year field's verbose name is "Year"."""
        self.assertEqual(
            self.model._meta.get_field("year").verbose_name, "Year"
        )

    def test_year_blank(self):
        """Test that the year field's blank is False."""
        self.assertEqual(self.model._meta.get_field("year").blank, False)

    def test_brand_verbose_name(self):
        """Test that the brand field's verbose name is "Brand"."""
        self.assertEqual(
            self.model._meta.get_field("brand").verbose_name, "Brand"
        )

    def test_brand_related_model(self):
        """Test that the brand field's related model is Brand."""
        self.assertEqual(
            self.model._meta.get_field("brand").related_model, Brand
        )

    def test_category_verbose_name(self):
        """Test that the category field's verbose name is "Category"."""
        self.assertEqual(
            self.model._meta.get_field("category").verbose_name, "Category"
        )

    def test_category_related_model(self):
        """Test that the category field's related model is Category."""
        self.assertEqual(
            self.model._meta.get_field("category").related_model, Category
        )


class ProductShotModelTest(
    ModelMetaOptionsTestMixin,
    ModelWithNameTestMixin,
    ModelWithDescriptionAndImageTestMixin,
    ModelWithFKToProductTestMixin,
    TestCase,
):
    """Test cases for the ProductShot model."""

    model = ProductShot
    ordering = ["name"]
    verbose_name = "Product shot"
    verbose_name_plural = "Product shots"
    # Redefined default parameter values of the abstract model(s).
    description_blank = True
    image_upload_to = "product_shots/"

    @classmethod
    def setUpTestData(cls) -> NoReturn:
        """Creates the first ProductShot for testing."""
        ProductShot.objects.create(
            name="test product shot",
            description="For the first product",
            image="./some_image.jpg",
            product=Product.objects.create(
                name="Test laptop",
                description="Some content",
                image="./some_image.jpg",
                price=1000,
                year=2023,
                brand=Brand.objects.create(name="test brand"),
                category=Category.objects.create(name="test category"),
            ),
        )


class LikeModelTest(
    ModelMetaOptionsTestMixin,
    ModelWithCreatedDateTimeTestMixin,
    ModelWithFKToProductTestMixin,
    SimpleTestCase,
):
    """Test cases for the Like model."""

    model = Like
    verbose_name = "Like"
    verbose_name_plural = "Likes"
    ordering = ["-created", "product_id"]

    def test_user_verbose_name(self):
        """Test that the user field's verbose name is "From user"."""
        self.assertEqual(
            self.model._meta.get_field("user").verbose_name, "From user"
        )

    def test_user_related_model(self):
        """Test that the user field's related model is Django User model."""
        self.assertEqual(
            self.model._meta.get_field("user").related_model, User
        )


class ReviewModelTest(
    ModelMetaOptionsTestMixin,
    ModelWithNameTestMixin,
    ModelWithCreatedDateTimeTestMixin,
    ModelWithFKToProductTestMixin,
    TestCase,
):
    """Test cases for the Review model."""

    model = Review
    verbose_name = "Review"
    verbose_name_plural = "Reviews"
    ordering = ["-created", "name", "product_id"]
    # Redefined default parameter values of the abstract model(s).
    name_verbose_name = "Username"

    @classmethod
    def setUpTestData(cls) -> NoReturn:
        """Creates the first Review for testing."""
        Review.objects.create(
            name="Test user",
            body="Some content",
            parent=None,
            product=Product.objects.create(
                name="Test laptop",
                description="Some content",
                image="./some_image.jpg",
                price=1000,
                year=2023,
                brand=Brand.objects.create(name="test brand"),
                category=Category.objects.create(name="test category"),
            ),
        )

    def test_model_string_representation(self):
        """Test the model string representation by __str__."""
        review = Review.objects.get(id=1)
        self.assertEqual(
            str(review), f"From {review.name} for {review.product}"
        )

    def test_body_verbose_name(self):
        """Test that the body field's verbose name is "Body"."""
        self.assertEqual(
            self.model._meta.get_field("body").verbose_name, "Body"
        )

    def test_body_blank(self):
        """Test that the body field's blank is False."""
        self.assertEqual(self.model._meta.get_field("body").blank, False)

    def test_parent_verbose_name(self):
        """Test that the parent field's verbose name is "Parent"."""
        self.assertEqual(
            self.model._meta.get_field("parent").verbose_name, "Parent"
        )

    def test_parent_related_model(self):
        """Test that the parent field's related model is self (Review)."""
        self.assertEqual(
            self.model._meta.get_field("parent").related_model, Review
        )

    def test_parent_null(self):
        """Test that the parent field's null is True."""
        self.assertEqual(self.model._meta.get_field("parent").null, True)
