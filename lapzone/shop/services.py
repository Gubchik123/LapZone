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


def get_all_products_that_contains_(
    user_input: str, products: QuerySet[models.Product]
) -> QuerySet[models.Product]:
    """Returns QuerySet with all products that contain user search input"""
    return products.filter(name__icontains=user_input)


def get_all_products_by_category_(slug: str) -> QuerySet[models.Product]:
    """Returns a QuerySet with all products by category slug."""
    return models.Product.objects.filter(category__slug=slug)


def get_all_products_by_brand_(slug: str) -> QuerySet[models.Product]:
    """Returns a QuerySet with all products by brand slug."""
    return models.Product.objects.filter(brand__slug=slug)
