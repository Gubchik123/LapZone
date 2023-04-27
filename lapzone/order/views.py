from django.views import generic
from django.db.models import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin

from . import services
from .models import Order
from general.views import BaseView


class OrderDetailView(BaseView, LoginRequiredMixin, generic.DetailView):
    """View for the order detail page."""

    model = Order
    template_name = "order/detail.html"

    def get_queryset(self):
        """Returns a queryset of orders that belong to the current user."""
        return super().get_queryset().filter(user=self.request.user)

    def get_object(self, queryset: QuerySet[Order] | None = None) -> Order:
        """
        Returns a user order from the given queryset by the 'pk' URL parameter.
        """
        return services.get_user_order_from_(
            queryset if queryset is not None else self.get_queryset(),
            self.kwargs["pk"],
        )
