import re
from typing import NoReturn

from django.db import models


class ModelWithName(models.Model):
    """Abstract model with 'name' CharField"""

    name = models.CharField(
        max_length=100, unique=True, blank=False, verbose_name="Name"
    )

    def __str__(self) -> str:
        """Gets string representation of a model."""
        return self.name

    class Meta:
        abstract = True


class ModelWithNameAndSlug(ModelWithName, models.Model):
    """Abstract model with 'name' CharField and 'slug' SlugField"""

    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=False,
        db_index=True,
        verbose_name="Slug",
    )

    def save(self, *args, **kwargs) -> None:
        """Saves the current instance"""
        self._generate_correct_slug()
        return super().save(*args, **kwargs)

    def _generate_correct_slug(self) -> NoReturn:
        """Sets correct slug from name"""
        self.slug = re.sub(
            pattern=r"[^\w+]", repl="-", string=self.name
        ).lower()

    class Meta:
        abstract = True


class ModelWithDescription(models.Model):
    """Abstract model with 'description' TextField"""

    description = models.TextField(blank=False, verbose_name="Description")

    class Meta:
        abstract = True


class ModelWithImage(models.Model):
    """Abstract model with 'image' ImageField"""

    image = models.ImageField(
        upload_to="content/", blank=False, verbose_name="Image"
    )

    class Meta:
        abstract = True


class ModelWithCreatedDateTime(models.Model):
    """Abstract model with 'created' DateTimeField"""

    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Created at"
    )

    class Meta:
        abstract = True


class ModelWithFKToProduct(models.Model):
    """Abstract model with 'product' ForeignKey field"""

    product = models.ForeignKey(
        "shop.Product",
        on_delete=models.CASCADE,
        verbose_name="For product",
    )

    class Meta:
        abstract = True
