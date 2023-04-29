from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import QuerySet
from django.http import HttpResponseRedirect, HttpRequest
from django.contrib.auth.mixins import LoginRequiredMixin

from . import services
from .models import Order
from general.views import BaseView


class OrderViewMixin(BaseView, LoginRequiredMixin):
    """Mixin for the order views."""

    model = Order

    def get_queryset(self):
        """Returns a queryset of orders that belong to the current user."""
        return super().get_queryset().filter(user=self.request.user)


class OrderListView(OrderViewMixin, generic.ListView):
    """View for the order list page."""


class OrderDetailView(OrderViewMixin, generic.DetailView):
    """View for the order detail page."""

    def get_object(self, queryset: QuerySet[Order] | None = None) -> Order:
        """
        Returns a user order from the given queryset by the 'pk' URL parameter.
        """
        return services.get_user_order_from_(
            queryset if queryset is not None else self.get_queryset(),
            self.kwargs["pk"],
        )


class OrderDeleteView(OrderDetailView, generic.DeleteView):
    """View for deleting an order."""

    http_method_names = ["post"]
    success_url = reverse_lazy("order:list")

    def post(
        self, request: HttpRequest, *args, **kwargs
    ) -> HttpResponseRedirect:
        """Adds a success message and calls the super().post() method."""
        messages.success(request, "Order has successfully deleted.")
        return super().post(request, *args, **kwargs)
