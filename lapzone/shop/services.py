from django.shortcuts import redirect
from django.db.models import QuerySet
from django.http import HttpResponseRedirect

from . import models
from .forms import ProductFilterForm


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


def check_and_get_redirect_response_by_(
    form: ProductFilterForm,
) -> HttpResponseRedirect | None:
    """Checks filter form and returns redirect response or None"""
    max_price = form.cleaned_data["max_price"]
    min_price = form.cleaned_data["min_price"]
    category = form.cleaned_data["category"]
    brands = form.cleaned_data["brands"]
    years = form.cleaned_data["years"]

    # If checked only the category in the form
    if category and not any([max_price, min_price, brands, years]):
        return redirect("shop:category", slug=category.slug)

    if (  # checked only one brand in the form
        brands
        and len(brands) == 1
        and not any([max_price, min_price, category, years])
    ):
        return redirect("shop:brand", slug=brands.first().slug)

    return None


def get_all_products_by_category_(slug: str) -> QuerySet[models.Product]:
    """Returns a QuerySet with all products by category slug."""
    return models.Product.objects.filter(category__slug=slug)


def get_all_products_by_brand_(slug: str) -> QuerySet[models.Product]:
    """Returns a QuerySet with all products by brand slug."""
    return models.Product.objects.filter(brand__slug=slug)
