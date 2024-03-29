from django.test import TestCase

from shop import models
from general.test_mixins.for_views import ProductTestMixin
from general.test_mixins.for_models import (
    ModelMetaOptionsTestMixin,
    ModelWithNameTestMixin,
    ModelWithNameAndSlugTestMixin,
    ModelWithDescriptionTestMixin,
    ModelWithImageTestMixin,
    ModelWithCreatedDateTimeTestMixin,
    ModelWithPriceTestMixin,
    ModelWithFKToProductTestMixin,
    ModelWithFKToUserTestMixin,
)


class BrandModelTestCase(
    ModelMetaOptionsTestMixin, ModelWithNameAndSlugTestMixin, TestCase
):
    """Test cases for the Brand model."""

    model = models.Brand
    ordering = ["name"]
    verbose_name = "Brand"
    verbose_name_plural = "Brands"
    # Redefined default parameter values of the abstract model(s).
    name_max_length = 30
    slug_max_length = 30

    url_pattern_name = "brand"

    expected_slug = "test-brand"
    expected_url = "/brand/test-brand/"

    @classmethod
    def setUpTestData(cls) -> None:
        """Creates the first Brand for testing."""
        models.Brand.objects.create(name="test brand")


class CategoryModelTestCase(
    ModelMetaOptionsTestMixin, ModelWithNameAndSlugTestMixin, TestCase
):
    """Test cases for the Category model."""

    model = models.Category
    ordering = ["name"]
    verbose_name = "Category"
    verbose_name_plural = "Categories"
    # Redefined default parameter values of the abstract model(s).
    name_max_length = 50
    slug_max_length = 50

    url_pattern_name = "category"

    expected_slug = "test-category"
    expected_url = "/category/test-category/"

    @classmethod
    def setUpTestData(cls) -> None:
        """Creates the first Category for testing."""
        models.Category.objects.create(name="test category")


class ModelWithDescriptionAndImageTestMixin(
    ModelWithDescriptionTestMixin, ModelWithImageTestMixin
):
    """
    Mixin for both ModelWithDescriptionTestMixin and ModelWithImageTestMixin
    """


class ProductModelTestCase(
    ProductTestMixin,
    ModelMetaOptionsTestMixin,
    ModelWithNameAndSlugTestMixin,
    ModelWithDescriptionAndImageTestMixin,
    ModelWithPriceTestMixin,
    TestCase,
):
    """Test cases for the Product model."""

    model = models.Product
    verbose_name = "Product"
    verbose_name_plural = "Products"
    ordering = ["name", "-price"]
    # Redefined default parameter values of the abstract model(s).
    image_upload_to = "products/"

    url_pattern_name = "product_detail"

    expected_slug = "test-product"
    expected_url = "/product/test-product/"
    expected_image_name = "test-product.webp"

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
            self.model._meta.get_field("brand").related_model, models.Brand
        )

    def test_brand_on_delete_cascade(self):
        """Test that the brand field's on_delete is CASCADE."""
        models.Product.objects.get(name="Test product").delete()
        with self.assertRaises(models.Brand.DoesNotExist):
            models.Brand.objects.get(id=1)

    def test_category_verbose_name(self):
        """Test that the category field's verbose name is "Category"."""
        self.assertEqual(
            self.model._meta.get_field("category").verbose_name, "Category"
        )

    def test_category_related_model(self):
        """Test that the category field's related model is Category."""
        self.assertEqual(
            self.model._meta.get_field("category").related_model,
            models.Category,
        )

    def test_category_on_delete_cascade(self):
        """Test that the category field's on_delete is CASCADE."""
        # * The first Product instance have already deleted above
        with self.assertRaises(models.Category.DoesNotExist):
            models.Category.objects.get(id=1)


class ProductShotModelTestCase(
    ProductTestMixin,
    ModelMetaOptionsTestMixin,
    ModelWithNameTestMixin,
    ModelWithDescriptionAndImageTestMixin,
    ModelWithFKToProductTestMixin,
    TestCase,
):
    """Test cases for the ProductShot model."""

    model = models.ProductShot
    ordering = ["name"]
    verbose_name = "Product shot"
    verbose_name_plural = "Product shots"
    # Redefined default parameter values of the abstract model(s).
    description_blank = True
    image_upload_to = "product_shots/"

    expected_image_name = "test-product-shot-1.webp"

    @classmethod
    def setUpTestData(cls) -> None:
        """Creates the first ProductShot for testing."""
        super().setUpTestData()
        models.ProductShot.objects.create(
            name="test product shot",
            description="For the first product",
            image="./some_image.jpg",
            product=cls.product,
        )


class LikeModelTestCase(
    ProductTestMixin,
    ModelMetaOptionsTestMixin,
    ModelWithCreatedDateTimeTestMixin,
    ModelWithFKToProductTestMixin,
    ModelWithFKToUserTestMixin,
    TestCase,
):
    """Test cases for the Like model."""

    model = models.Like
    verbose_name = "Like"
    verbose_name_plural = "Likes"
    ordering = ["-created", "product_id"]

    @classmethod
    def setUpTestData(cls) -> None:
        """Creates the first Like for testing."""
        super().setUpTestData()
        models.Like.objects.create(
            user=models.User.objects.create(
                username="Someone", email="test@test.com", password="123"
            ),
            product=cls.product,
        )

    def test_model_string_representation(self):
        """Test the model string representation by __str__."""
        like = models.Like.objects.first()
        self.assertEqual(str(like), f"From {like.user} for {like.product}")


class ReviewModelTestCase(
    ProductTestMixin,
    ModelMetaOptionsTestMixin,
    ModelWithNameTestMixin,
    ModelWithCreatedDateTimeTestMixin,
    ModelWithFKToProductTestMixin,
    TestCase,
):
    """Test cases for the Review model."""

    model = models.Review
    verbose_name = "Review"
    verbose_name_plural = "Reviews"
    ordering = ["-created", "name", "product_id"]
    # Redefined default parameter values of the abstract model(s).
    name_max_length = 30
    name_verbose_name = "Username"

    @classmethod
    def setUpTestData(cls) -> None:
        """Creates the first Review for testing."""
        super().setUpTestData()
        models.Review.objects.create(
            name="Test user",
            body="Some content",
            parent=None,
            product=cls.product,
        )

    def test_model_string_representation(self):
        """Test the model string representation by __str__."""
        review = models.Review.objects.get(id=1)
        self.assertEqual(
            str(review), f"From {review.name} for {review.product}"
        )

    def test_name_unique(self):
        pass

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
            self.model._meta.get_field("parent").related_model, models.Review
        )

    def test_parent_blank(self):
        """Test that the parent field's blank is True."""
        self.assertEqual(self.model._meta.get_field("parent").blank, True)

    def test_parent_null(self):
        """Test that the parent field's null is True."""
        self.assertEqual(self.model._meta.get_field("parent").null, True)


class CarouselImageModelTestCase(
    ProductTestMixin,
    ModelMetaOptionsTestMixin,
    ModelWithNameTestMixin,
    ModelWithDescriptionAndImageTestMixin,
    ModelWithFKToProductTestMixin,
    TestCase,
):
    """Test cases for the CarouselImage model."""

    model = models.CarouselImage
    ordering = ["name"]
    verbose_name = "Carousel image"
    verbose_name_plural = "Carousel images"
    # Redefined default parameter values of the abstract model(s).
    description_blank = True
    image_upload_to = "carousel_images/"

    expected_image_name = "test carousel image.webp"

    @classmethod
    def setUpTestData(cls) -> None:
        """Creates the first CarouselImage for testing."""
        super().setUpTestData()
        models.CarouselImage.objects.create(
            name="test carousel image",
            image="./some_image.jpg",
            product=cls.product,
        )

    def test_product_blank(self):
        """Test that the product field can be blank."""
        self.assertTrue(self.model._meta.get_field("product").blank)

    def test_product_null(self):
        """Test that the product field can be null."""
        self.assertTrue(self.model._meta.get_field("product").null)
