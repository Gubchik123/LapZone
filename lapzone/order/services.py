from uuid import uuid4, UUID
from typing import NoReturn

from django.conf import settings
from django.contrib import messages
from django.db.models import QuerySet
from django.contrib.auth import login
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import Http404, HttpRequest
from allauth.account.models import EmailAddress
from django.template.loader import render_to_string
from allauth.account.utils import send_email_confirmation

from .forms import OrderCreateModelForm
from .models import Order, OrderItem
from cart.cart import Cart


def _send_email_to_customer_by_(
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


def _get_or_create_user(
    request: HttpRequest, form: OrderCreateModelForm
) -> User | None:
    """Returns a user if the user is authenticated or
    creates a new user if 'is_create_profile' is True."""
    if request.user.is_authenticated:
        return user
    elif form.cleaned_data["is_create_profile"]:
        user, was_created = _get_or_create_user_with_data_from_(form)
        if was_created:
            send_email_confirmation(request, user)
        login(
            request, user, backend="django.contrib.auth.backends.ModelBackend"
        )
        messages.success(
            request, f"Successfully signed in as {user.username}."
        )
        return user
    return None


def _get_or_create_user_with_data_from_(
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


def _create_order_for_user_with_data_from_(
    cart: Cart, user: User, order_id: UUID
) -> str:
    """
    Creates an order for the given user with the data from the given cart.
    Returns the absolute url of the created order.
    """
    order = Order.objects.create(
        id=order_id, user=user, total_price=cart.get_total_price()
    )
    for item_dict in cart:
        OrderItem.objects.create(
            order=order,
            product=item_dict["product"],
            quantity=item_dict["quantity"],
            price=item_dict["price"],
        )
    return order.get_absolute_url()


def process_order_and_get_redirect_url(
    request: HttpRequest, form: OrderCreateModelForm
) -> str:
    """Processes an order by the given form and returns the redirect url."""
    order_id = uuid4()
    _send_email_to_customer_by_(
        form.cleaned_data.get("email", None) or request.user.email,
        order_id,
        request,
    )
    redirect_url = "/"
    cart = Cart(request.session)
    if (user := _get_or_create_user(request, form)) is not None:
        redirect_url = _create_order_for_user_with_data_from_(
            cart, user, order_id
        )
        messages.success(request, "Order has successfully created.")
    cart.clear()
    return redirect_url


def get_user_order_from_(queryset: QuerySet, pk: UUID) -> Order | NoReturn:
    """Returns an order from the given queryset by the given pk (UUID)."""
    try:
        return queryset.get(pk=pk)
    except Order.DoesNotExist:
        raise Http404
