from uuid import UUID
from typing import NoReturn

from django.conf import settings
from django.contrib import messages
from django.db.models import QuerySet
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import Http404, HttpRequest
from allauth.account.models import EmailAddress
from django.template.loader import render_to_string

from .models import Order
from .forms import OrderCreateModelForm


def send_email_to_customer_by_(
    email: str, order_id: UUID, request: HttpRequest
) -> None:
    """Sends a receipt email to the customer at the given email address."""
    messages.info(request, f"We've just sent a receipt email to {email}")
    send_mail(
        "Thank you for your order from LapZone!",
        "Your order has been received and is currently being processed.",
        settings.EMAIL_HOST_USER,
        [email],
        html_message=render_to_string(
            "order/email.html",
            {
                "email": email,
                "order_id": order_id,
            },
            request=request,
        ),
    )


def get_or_create_user_with_data_from_(
    form: OrderCreateModelForm,
) -> tuple[User, bool]:
    """Returns a user with the data from the given OrderCreateModelForm."""
    user, was_created = User.objects.get_or_create(
        email=form.cleaned_data["email"]
    )
    if was_created:
        user.username = form.cleaned_data["username"]
        user.set_password(form.cleaned_data["password"])
        EmailAddress.objects.create(user=user, email=user.email)
    user.first_name = form.cleaned_data["first_name"]
    user.last_name = form.cleaned_data["last_name"]
    user.save()
    return user, was_created


def get_user_order_from_(queryset: QuerySet, pk: UUID) -> Order | NoReturn:
    """Returns an order from the given queryset by the given pk (UUID)."""
    try:
        return queryset.get(pk=pk)
    except Order.DoesNotExist:
        raise Http404
