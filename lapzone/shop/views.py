from typing import Any

from django.views import generic
from django.db.models import QuerySet
from django.http import HttpResponse, HttpRequest

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
        """Adds filter form in context data and returns it."""
        context = super().get_context_data(**kwargs)
        context["filter_form"] = ProductFilterForm(self.request.POST)
        return context


class AllProductsListView(_ProductListView):
    """View for displaying all or filtered products."""

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Adds page title in context data and returns it."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"All products"
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Checks form is valid and renders page with products."""
        form = ProductFilterForm(request.POST)
        context = self.get_context_data(**kwargs)
        context["page_title"] = "Filtered products"

        if form.is_valid():
            context["products"] = form.get_filtered_products()
        return self.render_to_response(context)


class SearchProductListView(_ProductListView):
    """View for displaying all products that contain user search input."""

    def get_queryset(self) -> QuerySet:
        """Returns QuerySet with products that contain user search input."""
        products = super().get_queryset()
        return services.get_all_products_that_contains_(
            self.request.GET["q"], products
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Adds page title in context data and returns it."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Search results for '{self.request.GET['q']}'"
        return context


class ProductListByCategoryView(_ProductListView):
    """View for displaying all products by category."""

    def get_queryset(self) -> QuerySet:
        """Returns QuerySet with products by category or raises 404."""
        slug = self.kwargs["slug"]
        return services.get_all_products_or_404_by_category_(slug)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Adds some content in context data and returns it."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.kwargs["slug"].capitalize()
        context["filter_form"] = ProductFilterForm(
            {"category": Category.objects.get(slug=self.kwargs["slug"])}
        )
        return context


class ProductListByBrandView(_ProductListView):
    """View for displaying all products by brand."""

    def get_queryset(self) -> QuerySet:
        """Returns QuerySet with products by brand or raises 404."""
        slug = self.kwargs["slug"]
        return services.get_all_products_or_404_by_brand_(slug)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Adds some content in context data and returns it."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"{self.kwargs['slug'].capitalize()} products"
        context["filter_form"] = ProductFilterForm(
            {"brands": Brand.objects.filter(slug=self.kwargs["slug"])}
        )
        return context
