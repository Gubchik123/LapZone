from PIL import Image

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify


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

    # Class attribute
    url_pattern_name: str

    # Model field.
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        db_index=True,
        verbose_name="Slug",
    )

    def save(self, *args, **kwargs):
        """Generates a slug for the instance if it does not already exist."""
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        """Returns the URL to page to display the detail of the instance."""
        return reverse(f"shop:{self.url_pattern_name}", args=[self.slug])

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

    def save(self, *args, **kwargs):
        """Changes the image name and optimize if it's allowed."""
        is_allow_to_resize_image = self._get_allow_for_image_resizing()
        super().save(*args, **kwargs)
        if (
            is_allow_to_resize_image
            and self.is_allow_to_resize
            and not settings.TESTING
        ):
            self._resize_and_optimize_image()

    def _get_allow_for_image_resizing(self) -> bool:
        """Checks instance and returns an allow for resizing after saving."""
        if self._is_not_new_instance():
            prev_instance = type(self).objects.get(pk=self.pk)
            if prev_instance.image != self.image:
                prev_instance.image.delete(save=False)
                return self._set_image_name_and_allow_resizing()
            return False
        else:  # if it's a new instance
            return self._set_image_name_and_allow_resizing()

    def _is_not_new_instance(self) -> bool:
        """Returns True if it's not a new instance and False if it is."""
        return self.pk is not None

    def _set_image_name_and_allow_resizing(self) -> True:
        """Sets image name to image_name attribute and allows resizing."""
        self.image.name = f"{self.image_name}.webp"
        return True

    def _resize_and_optimize_image(self) -> None:
        """Resizes the image if it's larger than 800px and optimizes."""
        img = Image.open(self.image)

        if img.width > 800:
            ratio = 800 / float(img.width)
            new_height = int(ratio * img.height)
            img = img.resize((800, new_height), Image.ANTIALIAS)

        img.save(self.image.path, "webp", quality=80, optimize=True)
        img.close()

    class Meta:
        abstract = True


class ModelWithCreatedDateTime(models.Model):
    """Abstract model with 'created' DateTimeField"""

    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Created datetime"
    )

    class Meta:
        abstract = True


class ModelWithFKToProduct(models.Model):
    """Abstract model with 'product' ForeignKey field"""

    product = models.ForeignKey(
        "shop.Product",
        on_delete=models.CASCADE,
        verbose_name="Product",
    )

    class Meta:
        abstract = True
