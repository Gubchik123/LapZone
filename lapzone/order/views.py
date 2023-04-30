from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import QuerySet
from django.http import HttpResponseRedirect, HttpRequest
from django.contrib.auth.mixins import LoginRequiredMixin

from . import services
from .models import Order
from .forms import OrderCreateForm
from general.views import BaseView


class OrderCreateFormView(BaseView, generic.FormView):
    """View for the checkout page."""

    form_class = OrderCreateForm
    template_name = "order/order_create.html"

    def get_initial(self):
        """
        Return the initial data to use for the OrderCreateForm.
        Checks if the user is authenticated and adds the user data.
        """
        if self.request.user.is_authenticated:
            return {
                "email": self.request.user.email,
                "first_name": self.request.user.first_name,
                "last_name": self.request.user.last_name,
            }
        return super().get_initial()

    def get_form(self, form_class=None):
        """
        Returns an instance of the form to be used in this view.
        Checks if the user is authenticated and removes the 'is_create_profile' field.
        """
        form = super().get_form(form_class)
        if self.request.user.is_authenticated:
            del form.fields["is_create_profile"]
        return form


class OrderViewMixin(BaseView, LoginRequiredMixin):
    """Mixin for the order views."""

    model = Order

    def get_queryset(self):
        """Returns a queryset of orders that belong to the current user."""
        return super().get_queryset().filter(user=self.request.user)


class OrderListView(OrderViewMixin, generic.ListView):
    """View for the order list page."""

    paginate_by = 10


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
