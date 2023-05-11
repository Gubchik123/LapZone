from typing import Any
from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect

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


class CustomerUpdateView(BaseView, generic.UpdateView):
    """View to handle the UserModelForm and update the customer data."""

    model = User
    form_class = UserModelForm
    http_method_names = ["post"]
    success_url = reverse_lazy("customer:detail")

    def get_object(self, queryset: QuerySet[User] | None = ...) -> User:
        """Returns the current user."""
        return self.request.user

    def form_valid(self, form: UserModelForm) -> HttpResponse:
        """Adds a success message and returns the super method."""
        messages.success(
            self.request, "Your personal data has successfully updated."
        )
        return super().form_valid(form)

    def form_invalid(self, form: UserModelForm) -> HttpResponse:
        """Adds form error messages and returns redirect to the success_url."""
        for error in form.errors.as_data().values():
            messages.error(self.request, error[0].messages[0])
        return HttpResponseRedirect(self.success_url)
