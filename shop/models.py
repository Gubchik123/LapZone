from typing import Any
from django.db import models
from django.contrib.auth.models import User

from general.models import (
    ModelWithName,
    ModelWithNameAndSlug,
    ModelWithDescription,
    ModelWithImage,
    ModelWithPrice,
    ModelWithCreatedDateTime,
    ModelWithFKToProduct,
    ModelWithFKToUser,
)


class Brand(ModelWithNameAndSlug, models.Model):
    """
    A model representing a product brand, for example, Asus.
    Fields: name, slug.
    """

    url_pattern_name = "brand"

    class Meta:
        """Meta options for the Brand model."""

        ordering = ["name"]
        verbose_name = "Brand"
        verbose_name_plural = "Brands"


# Redefining an abstract model field parameters
Brand._meta.get_field("name").max_length = 30
Brand._meta.get_field("slug").max_length = 30


class Category(ModelWithNameAndSlug, models.Model):
    """
    A model representing a product category, for example, laptops.
    Fields: name, slug.
    """

    url_pattern_name = "category"

    class Meta:
        """Meta options for the Category model."""

        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"


# Redefining an abstract model field parameters
Category._meta.get_field("name").max_length = 50
Category._meta.get_field("slug").max_length = 50


class ModelWithDescriptionAndImage(ModelWithDescription, ModelWithImage):
    """Abstract model with 'description' TextField and 'image' ImageField."""

    class Meta:
        abstract = True


class Product(
    ModelWithNameAndSlug,
    ModelWithDescriptionAndImage,
    ModelWithPrice,
    models.Model,
):
    """
    A model representing a product, for example, 'ASUS ROG Zephyrus M16'.
    Fields: name, slug, description, image, price, year, brand, category.
    """

    # Class attribute
    url_pattern_name = "product_detail"

    # Model fields
    year = models.IntegerField(blank=False, verbose_name="Year")

    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, verbose_name="Brand"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Category"
    )

    def save(self, *args, **kwargs):
        """Sets the special attributes for the parent save method."""
        self.is_allow_to_resize = True
        self.image_name = self.slug
        super().save(*args, **kwargs)

    class Meta:
        """Meta options for the Product model."""

        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["name", "-price"]


# Redefining an abstract model field parameter
Product._meta.get_field("image").upload_to = "products/"


class ProductShot(
    ModelWithName,
    ModelWithDescriptionAndImage,
    ModelWithFKToProduct,
    models.Model,
):
    """
    A model representing a product shot.
    Fields: name, description, image, product.
    """

    def save(self, *args, **kwargs):
        """Sets the special attributes for the parent save method."""
        self.is_allow_to_resize = True
        shots_count = self.product.productshot_set.count() + 1
        self.image_name = f"{self.product.slug}-shot-{shots_count}"
        super().save(*args, **kwargs)

    class Meta:
        """Meta options for the ProductShot model."""

        ordering = ["name"]
        verbose_name = "Product shot"
        verbose_name_plural = "Product shots"


# Redefining an abstract model field parameters
ProductShot._meta.get_field("description").blank = True
ProductShot._meta.get_field("image").upload_to = "product_shots/"


class ModelWithCreatedDateTimeAndFKToProduct(
    ModelWithCreatedDateTime, ModelWithFKToProduct, models.Model
):
    """
    Abstract model with 'created' DateTimeField and 'product' ForeignKey field
    """

    class Meta:
        abstract = True


class Like(
    ModelWithCreatedDateTimeAndFKToProduct, ModelWithFKToUser, models.Model
):
    """
    A model representing a product like from user.
    Fields: created, product, user.
    """

    def __str__(self) -> str:
        """Gets string representation of the Like model."""
        return f"From {self.user} for {self.product}"

    class Meta:
        """Meta options for the Like model."""

        verbose_name = "Like"
        verbose_name_plural = "Likes"
        ordering = ["-created", "product_id"]


class _ReviewCustomManager(models.Manager):
    """Custom manager for the Review model."""

    def all(self):
        """Returns all reviews using the select_related for the 'parent'."""
        return super().all().select_related("parent")


class Review(
    ModelWithCreatedDateTimeAndFKToProduct,
    models.Model,
):
    """
    A model representing a product review from someone.
    Fields: username, body, created, parent, product.
    """

    name = models.CharField(
        max_length=30, blank=False, verbose_name="Username"
    )
    body = models.TextField(blank=False, verbose_name="Body")

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="Parent",
    )

    objects = _ReviewCustomManager()

    def __str__(self) -> str:
        """Gets string representation of the Review model."""
        return f"From {self.name} for {self.product}"

    class Meta:
        """Meta options for the Review model."""

        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ["-created", "name", "product_id"]


class CarouselImage(
    ModelWithName,
    ModelWithDescriptionAndImage,
    ModelWithFKToProduct,
    models.Model,
):
    """
    A model representing a carousel image.
    Fields: name, description, image, product.
    """

    def save(self, *args, **kwargs):
        """Sets the special attributes for the parent save method."""
        self.is_allow_to_resize = False
        self.image_name = self.name
        super().save(*args, **kwargs)

    class Meta:
        """Meta options for the CarouselImage model."""

        ordering = ["name"]
        verbose_name = "Carousel image"
        verbose_name_plural = "Carousel images"


# Redefining an abstract model field parameters
CarouselImage._meta.get_field("description").blank = True
CarouselImage._meta.get_field("image").upload_to = "carousel_images/"
CarouselImage._meta.get_field("product").blank = True
CarouselImage._meta.get_field("product").null = True
