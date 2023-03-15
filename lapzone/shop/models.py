from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from general.models import (
    ModelWithName,
    ModelWithNameAndSlug,
    ModelWithDescription,
    ModelWithImage,
    ModelWithCreatedDateTime,
    ModelWithForeignKeyToProduct,
)


class Brand(ModelWithNameAndSlug, models.Model):
    """
    A model representing a product brand, for example, Asus.
    Fields: name, slug
    """

    # TODO: For now, there is no such view name.
    # def get_absolute_url(self):
    #     """Gets the URL to page for displaying the detail of a brand."""
    #     return reverse("shop:brand_detail", args=[self.slug])

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
    Fields: name, slug
    """

    # TODO: For now, there is no such view name.
    # def get_absolute_url(self):
    #     """Gets the URL to page for displaying the detail of a category."""
    #     return reverse("shop:category_detail", args=[self.slug])

    class Meta:
        """Meta options for the Category model."""

        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"


# Redefining an abstract model field parameters
Category._meta.get_field("name").max_length = 50
Category._meta.get_field("slug").max_length = 50


class ModelWithDescriptionAndImage(ModelWithDescription, ModelWithImage):
    """Abstract model with 'description' TextField and 'image' ImageField"""

    class Meta:
        abstract = True


class Product(
    ModelWithNameAndSlug, ModelWithDescriptionAndImage, models.Model
):
    """
    A model representing a product, for example, 'ASUS ROG Zephyrus M16'.
    Fields: name, slug, description, image, price, year, brand, category
    """

    price = models.FloatField(blank=False, verbose_name="Price")
    year = models.IntegerField(blank=False, verbose_name="Year")

    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, verbose_name="Brand"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Category"
    )

    # TODO: For now, there is no such view name.
    # def get_absolute_url(self):
    #     """Gets the URL to page for displaying the detail of a product."""
    #     return reverse("shop:product_detail", args=[self.slug])

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
    ModelWithForeignKeyToProduct,
    models.Model,
):
    """
    A model representing a product shot.
    Fields: name, description, image, product
    """

    class Meta:
        """Meta options for the ProductShot model."""

        ordering = ["name"]
        verbose_name = "Product shot"
        verbose_name_plural = "Product shots"


# Redefining an abstract model field parameters
ProductShot._meta.get_field("description").blank = True
ProductShot._meta.get_field("image").upload_to = "product_shots/"


class ModelWithCreatedDateTimeAndForeignKeyToProduct(
    ModelWithCreatedDateTime, ModelWithForeignKeyToProduct, models.Model
):
    """
    Abstract model with 'created' DateTimeField and 'product' ForeignKey field
    """

    class Meta:
        abstract = True


class Like(ModelWithCreatedDateTimeAndForeignKeyToProduct, models.Model):
    """
    A model representing a product like from user.
    Fields: created, user, product
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="From user"
    )

    def __str__(self) -> str:
        """Gets string representation of the Like model."""
        return f"From {self.user} for {self.product}"

    class Meta:
        """Meta options for the Like model."""

        verbose_name = "Like"
        verbose_name_plural = "Likes"
        ordering = ["-created", "product_id"]


class Review(
    ModelWithName,
    ModelWithCreatedDateTimeAndForeignKeyToProduct,
    models.Model,
):
    """
    A model representing a product review from someone.
    Fields: name (username), body, created, parent, product
    """

    body = models.TextField(blank=False, verbose_name="Body")

    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, verbose_name="Parent"
    )

    def __str__(self) -> str:
        """Gets string representation of the Review model."""
        return f"From {self.name} for {self.product}"

    class Meta:
        """Meta options for the Review model."""

        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ["-created", "name", "product_id"]


# Redefining an abstract model field parameter
Review._meta.get_field("name").verbose_name = "Username"
