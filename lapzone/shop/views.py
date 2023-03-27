from typing import Any

from django.views import generic
from django.db.models import QuerySet
from django.core.exceptions import FieldError
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

from general.views import BaseView
from . import services
from .forms import ProductFilterForm
from .models import Product, Category, Brand


class HomeView(BaseView, generic.TemplateView):
    """View for the home page and the "/" site URL."""

    template_name = "shop/home.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Adds some content in context data and returns it."""
        context = super().get_context_data(**kwargs)
        context["brands"] = services.get_all_brands()
        context["categories"] = services.get_all_categories()
        context["carousel_images"] = services.get_all_carousel_images()
        return context


class _ProductListView(BaseView, generic.ListView):
    """Base ListView for displaying all products with filter form."""

    model = Product
    context_object_name = "products"
    object_list = Product.objects.all()

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Redefines context["products"] with ordered ones or the same"""
        context = super().get_context_data(**kwargs)
        context["products"] = self._get_ordered_(context["products"])
        return context

    def _get_ordered_(self, products: QuerySet[Product]) -> QuerySet[Product]:
        """
        Returns a sorted QuerySet of products based on GET parameters.
        If there are some exceptions, returns the original QuerySet.
        """
        order_by = self.request.GET.get("orderby")
        order_dir = self.request.GET.get("orderdir")

        if order_by and order_dir:
            try:
                return services.get_ordered_products_by_(
                    order_by, order_dir, products
                )
            except (FieldError, services.UnknownOrderDirection):
                return []
        return products


class AllProductsListView(_ProductListView):
    """View for displaying all or filtered products."""

    def get_queryset(self) -> QuerySet[Product]:
        """Returns QuerySet with products."""
        user_search_input = self.request.GET.get("q", None)
        products = super().get_queryset()

        if user_search_input is not None:
            products = services.get_all_products_that_contains_(
                user_search_input, products
            )
        return products

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Adds page title in context data and returns it."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"All products"
        context["filter_form"] = ProductFilterForm(self.request.POST)

        user_search_input = self.request.GET.get("q", None)

        if user_search_input is not None:
            context["page_title"] = f"Search results for '{user_search_input}'"
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Checks form is valid and renders page with products."""
        form = ProductFilterForm(request.POST)
        context = self.get_context_data(**kwargs)
        context["page_title"] = "Filtered products"

        if form.is_valid():
            response: HttpResponseRedirect | None = (
                services.check_and_get_redirect_response_by_(form)
            )
            if response is not None:
                return response
            context["products"] = self._get_ordered_(
                products=form.get_filtered_products()
            )
        return self.render_to_response(context)


class ProductListByCategoryView(_ProductListView):
    """View for displaying all products by category."""

    def get_queryset(self) -> QuerySet[Product]:
        """Returns QuerySet with all products by category."""
        return services.get_all_products_by_category_(self.kwargs["slug"])

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Adds some content in context data and returns it."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.kwargs["slug"].capitalize()
        context["filter_form"] = ProductFilterForm(
            {"category": get_object_or_404(Category, slug=self.kwargs["slug"])}
        )
        return context


class ProductListByBrandView(_ProductListView):
    """View for displaying all products by brand."""

    def get_queryset(self) -> QuerySet[Product]:
        """Returns QuerySet with all products by brand."""
        return services.get_all_products_by_brand_(self.kwargs["slug"])

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Adds some content in context data and returns it."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"{self.kwargs['slug'].capitalize()} products"
        context["filter_form"] = ProductFilterForm(
            {"brands": [get_object_or_404(Brand, slug=self.kwargs["slug"])]}
        )
        return context
