from typing import NoReturn

from django.http import Http404
from django.db.models import QuerySet

from . import models


def get_all_brands() -> QuerySet[models.Brand]:
    """Returns QuerySet with all brands."""
    return models.Brand.objects.all()


def get_all_categories() -> QuerySet[models.Category]:
    """Returns QuerySet with all categories."""
    return models.Category.objects.all()


def get_all_carousel_images() -> QuerySet[models.CarouselImage]:
    """Returns QuerySet with all carousel images."""
    return models.CarouselImage.objects.all()


def _get_all_or_404_(
    products: QuerySet[models.Product],
) -> QuerySet[models.Product] | NoReturn:
    """Return the given QuerySet if exist or raises 404."""
    if products.exists():
        return products
    raise Http404


def get_all_products_or_404_by_category_(
    slug: str,
) -> QuerySet[models.Product]:
    """Returns a QuerySet with all products by the given slug or raises 404."""
    return _get_all_or_404_(models.Product.objects.filter(category__slug=slug))


def get_all_products_or_404_by_brand_(slug: str) -> QuerySet[models.Product]:
    """Returns a QuerySet with all products by the given slug or raises 404."""
    return _get_all_or_404_(models.Product.objects.filter(brand__slug=slug))
