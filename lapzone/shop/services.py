import json
import logging

from django.shortcuts import redirect
from django.db.models import QuerySet
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from . import models
from .forms import ProductFilterForm, ReviewForm


logger = logging.getLogger(__name__)


def get_recently_added_products(count: int) -> QuerySet[models.Product]:
    """Returns the given number of recently added products."""
    return models.Product.objects.order_by("-id")[:count]


def get_liked_products_for_(user: User) -> list[int]:
    """Returns a list of IDs for all products liked by the given user."""
    return [tup[0] for tup in user.like_set.all().values_list("product_id")]


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
    if review_parent_id:
        review.parent_id = int(review_parent_id)
    review.save()


def _get_user_id_from_(request_body: bytes) -> int:
    """Extracts and returns the user ID from a JSON request body."""
    data = json.loads(request_body)
    try:
        return int(data["user_id"])
    except KeyError:
        return None


def add_or_delete_like_and_get_response_message(
    request_body: bytes, product_slug: str
) -> str:
    """
    Adds or deletes a 'like' record
    for the given product slug and user ID and returns a response message.
    """
    user_id = _get_user_id_from_(request_body)

    if not (product_slug and user_id):
        logger.error(
            f"like processing: product_slug={product_slug}, user_id={user_id}"
        )
        return "There was an error! Try again later."

    like, was_created = models.Like.objects.get_or_create(
        user_id=user_id,
        product_id=models.Product.objects.get(slug=product_slug).id,
    )

    if not was_created:
        like.delete()
        message_prefix = "deleted from"
    else:
        message_prefix = "added to"

    return f"Product has successfully {message_prefix} your wish list."
