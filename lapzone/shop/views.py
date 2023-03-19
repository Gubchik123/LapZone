from typing import Any

from django.views.generic import TemplateView

from . import services
from general.views import BaseView


class HomeView(BaseView, TemplateView):
    template_name = "shop/home.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["brands"] = services.get_all_brands()
        context["categories"] = services.get_all_categories()
        context["carousel_images"] = services.get_all_carousel_images()
        return context
