from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_mail_to_(email: str) -> None:
    """Sends an email to the given email address."""
    subject_prefix = settings.ACCOUNT_EMAIL_SUBJECT_PREFIX
    send_mail(
        f"{subject_prefix}You have successfully subscribed to our mailing",
        "You will be noticed about all our changes.",
        settings.EMAIL_HOST_USER,
        [email],
        html_message=render_to_string("mailing/email.html", {"email": email}),
    )
