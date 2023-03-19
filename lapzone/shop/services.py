from django.db.models import QuerySet

from . import models


def get_all_brands() -> QuerySet:
    """Returns QuerySet with all brands."""
    return models.Brand.objects.all()


def get_all_categories() -> QuerySet:
    """Returns QuerySet with all categories."""
    return models.Category.objects.all()


def get_all_carousel_images() -> QuerySet:
    """Returns QuerySet with all carousel images."""
    return models.CarouselImage.objects.all()
