from typing import Any
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from general.views import BaseView
from .forms import UserModelForm


class CustomerDetailView(BaseView, LoginRequiredMixin, generic.TemplateView):
    """View for the customer detail page."""

    template_name = "customer/detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Adds the UserModelForm to the context and returns it."""
        context = super().get_context_data(**kwargs)
        context["form"] = UserModelForm(instance=self.request.user)
        return context
