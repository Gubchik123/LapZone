from django.conf import settings
from django.http import HttpRequest
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import MailingEmailAddress


def send_mail_to_(mailing_email_address: MailingEmailAddress, request: HttpRequest) -> None:
    """Sends an email to the given email address."""
    subject_prefix = settings.ACCOUNT_EMAIL_SUBJECT_PREFIX
    send_mail(
        f"{subject_prefix}You have successfully subscribed to our mailing",
        "You will be noticed about all our changes.",
        settings.EMAIL_HOST_USER,
        [mailing_email_address.email],
        html_message=render_to_string(
            "mailing/email.html",
            {
                "pk": mailing_email_address.pk,
                "email": mailing_email_address.email,
            },
            request,
        ),
    )
