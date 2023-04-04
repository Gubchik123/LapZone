from typing import Any

from django.views import generic
from django.contrib import messages
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

from general.views import BaseView
from . import services
from .models import Product, Category, Brand
from .forms import ProductFilterForm, ReviewForm


class HomeView(BaseView, generic.TemplateView):
    """View for the home page and the "/" site URL."""

    template_name = "shop/home.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Adds some content in context data and returns it."""
        context = super().get_context_data(**kwargs)
        context[
            "recently_added_products"
        ] = services.get_recently_added_products(10)
        context["brands"] = services.get_all_brands()
        context["categories"] = services.get_all_categories()
        context["carousel_images"] = services.get_all_carousel_images()
        return context


class _ProductListView(BaseView, generic.ListView):
    """Base ListView for displaying products."""

    model = Product
    paginate_by = 12
    object_list = Product.objects.all()

    def get_ordering(self) -> list[str]:
        """Returns list of ordering after checking GET parameters"""
        order_by = self.request.GET.get("orderby")
        order_dir = self.request.GET.get("orderdir")

        if services.are_ordering_parameters_valid(order_by, order_dir):
            return [services.get_order_symbol_by_(order_dir) + order_by]
        return []


class AllProductsListView(_ProductListView):
    """View for displaying all or filtered or searched products."""

    def get_queryset(self) -> QuerySet[Product]:
        """Returns QuerySet with either searched or filtered products."""
        user_search_input = self.request.GET.get("q", None)
        form = ProductFilterForm(self.request.POST)
        products = super().get_queryset()

        if user_search_input is not None:
            products = services.get_products_that_contains_(
                user_search_input, products
            )
        if form.is_valid():
            products = form.get_filtered_(products)

        return products

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Adds page title and filter form in context data and returns it."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "All products"
        context["filter_form"] = ProductFilterForm(self.request.POST)
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Checks form is valid and renders page with products."""
        form = ProductFilterForm(request.POST)

        if form.is_valid():
            response: HttpResponseRedirect | None = (
                services.check_and_get_redirect_response_by_(form)
            )
            if response is not None:
                return response
        return self.get(request, *args, **kwargs)


class ProductListByCategoryView(_ProductListView):
    """View for displaying products by category."""

    def get_queryset(self) -> QuerySet[Product]:
        """Returns QuerySet with products by category slug."""
        return services.get_products_filtered_by_category_(
            self.kwargs["slug"], products=super().get_queryset()
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Adds page title and filter form in context data and returns it."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.kwargs["slug"].capitalize()
        context["filter_form"] = ProductFilterForm(
            {"category": get_object_or_404(Category, slug=self.kwargs["slug"])}
        )
        return context


class ProductListByBrandView(_ProductListView):
    """View for displaying products by brand."""

    def get_queryset(self) -> QuerySet[Product]:
        """Returns QuerySet with products by brand slug."""
        return services.get_products_filtered_by_brand_(
            self.kwargs["slug"], products=super().get_queryset()
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Adds page title and filter form in context data and returns it."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"{self.kwargs['slug'].capitalize()} products"
        context["filter_form"] = ProductFilterForm(
            {"brands": [get_object_or_404(Brand, slug=self.kwargs["slug"])]}
        )
        return context


class ProductDetailView(BaseView, generic.DetailView):
    """View for displaying detailed information about a single product."""

    model = Product

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["review_form"] = ReviewForm()
        return context


class ReviewFormView(generic.FormView):
    """Form view for adding review to product."""

    form_class = ReviewForm

    def get_success_url(self) -> str:
        """Returns the URL to the product_detail page
        from which the POST request was made."""
        return self.request.path[:-7]  # path - "review/"

    def form_valid(self, form: ReviewForm) -> HttpResponseRedirect:
        """Adds success message, creates review
        and returns redirect to product_detail page."""
        review_parent_id = self.request.POST.get("review_parent_id", None)
        services.create_review_with_data_from_(
            form,
            product_slug=self.kwargs["slug"],
            review_parent_id=review_parent_id,
        )
        prefix = "Review" if review_parent_id is None else "Answer"
        messages.success(self.request, f"{prefix} has added successfully.")
        return super().form_valid(form)

    def form_invalid(self, form: ReviewForm) -> HttpResponseRedirect:
        """Adds error message and returns redirect to product_detail page."""
        prefix = (
            "Review"
            if self.request.POST.get("id_parent", None) is None
            else "Answer"
        )
        messages.error(
            self.request,
            f"Data in form is invalid! {prefix} has not added successfully.",
        )
        return HttpResponseRedirect(self.get_success_url())
