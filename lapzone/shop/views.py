from typing import Any

from django.views import generic
from django.db.models import QuerySet

from . import services
from .models import Product
from general.views import BaseView


class HomeView(BaseView, generic.TemplateView):
    """View for the home page and the "/" site URL"""

    template_name = "shop/home.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Adds some content in context data and returns it"""
        context = super().get_context_data(**kwargs)
        context["brands"] = services.get_all_brands()
        context["categories"] = services.get_all_categories()
        context["carousel_images"] = services.get_all_carousel_images()
        return context


class SearchProductListView(BaseView, generic.ListView):
    """View for displaying all products by user searching input"""

    model = Product
    context_object_name = "products"

    def get_queryset(self) -> QuerySet:
        """Returns QuerySet or raises 404."""
        return services.get_all_products_that_contains_(self.request.GET["q"])
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Adds page title in context data and returns it"""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Results"
        return context
    

class CategoryDetailListView(BaseView, generic.ListView):
    """View for displaying all products by category"""

    model = Product
    context_object_name = "products"

    def get_queryset(self) -> QuerySet:
        """Returns QuerySet or raises 404."""
        slug = self.kwargs["slug"]
        return services.get_all_products_or_404_by_category_(slug)
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Adds page title in context data and returns it"""
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.kwargs["slug"].capitalize()
        return context


class BrandDetailListView(BaseView, generic.ListView):
    """View for displaying all products by brand"""

    model = Product
    context_object_name = "products"

    def get_queryset(self) -> QuerySet:
        """Returns QuerySet or raises 404."""
        slug = self.kwargs["slug"]
        return services.get_all_products_or_404_by_brand_(slug)
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Adds page title in context data and returns it"""
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"{self.kwargs['slug'].capitalize()} products"
        return context
