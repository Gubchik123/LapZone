from django.shortcuts import redirect
from django.db.models import QuerySet
from django.http import HttpResponseRedirect

from . import models
from .forms import ProductFilterForm, ReviewForm


def get_recently_added_products(count: int) -> QuerySet[models.Product]:
    """Returns the given number of recently added products."""
    return models.Product.objects.order_by("-id")[:count]


def get_all_brands() -> QuerySet[models.Brand]:
    """Returns a QuerySet with all brands."""
    return models.Brand.objects.all()


def get_all_categories() -> QuerySet[models.Category]:
    """Returns a QuerySet with all categories."""
    return models.Category.objects.all()


def get_all_carousel_images() -> QuerySet[models.CarouselImage]:
    """Returns a QuerySet with all carousel images."""
    return models.CarouselImage.objects.all()


def are_ordering_parameters_valid(order_by: str, order_dir: str) -> bool:
    """Checks if the given order_by and order_dir are valid"""
    if (
        # there are not order_by and order_dir
        (not order_by and not order_dir)
        # there is order_by but there is not order_dir
        or (order_by and not order_dir)
        # there is order_dir but there is not order_by
        or (order_dir and not order_by)
        or (order_dir not in ("asc", "desc"))
        or (order_by not in ("name", "price"))
    ):
        return False
    return True


def get_order_symbol_by_(order_dir: str) -> str:
    """Returns the Django order symbol."""
    return "-" if order_dir == "desc" else ""


def get_products_that_contains_(
    user_input: str, products: QuerySet[models.Product]
) -> QuerySet[models.Product]:
    """Returns the given products filtered by user search input"""
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


def get_products_filtered_by_category_(
    slug: str, products: QuerySet[models.Product]
) -> QuerySet[models.Product]:
    """Returns the given products filtered by category slug."""
    return products.filter(category__slug=slug)


def get_products_filtered_by_brand_(
    slug: str, products: QuerySet[models.Product]
) -> QuerySet[models.Product]:
    """Returns the given products filtered by brand slug."""
    return products.filter(brand__slug=slug)


def create_review_with_data_from_(
    form: ReviewForm, product_slug: str, review_parent_id: str | None
) -> None:
    """Saves model form (creates review) with product by the given slug."""
    review: models.Review = form.save(commit=False)
    review.product = models.Product.objects.get(slug=product_slug)
    if review_parent_id is not None:
        review.parent_id = int(review_parent_id)
    review.save()
