from django.http import HttpRequest

from .forms import MailingEmailAddressModelForm


def mailing_form(
    request: HttpRequest,
) -> dict[str, MailingEmailAddressModelForm]:
    """Returns a dictionary with the MailingEmailAddressModelForm."""
    return {"mailing_form": MailingEmailAddressModelForm()}
