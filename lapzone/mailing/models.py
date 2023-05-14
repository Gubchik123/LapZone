from django.db import models

from general.models import ModelWithUUIDPK, ModelWithCreatedDateTime


class MailingEmailAddress(
    ModelWithUUIDPK, ModelWithCreatedDateTime, models.Model
):
    """
    A model representing an email address for mailing.
    Fields: id (uuid4), created, email.
    """

    email = models.EmailField(
        "Email address", unique=True, blank=False, null=False
    )

    class Meta:
        ordering = ["-created"]
        verbose_name = "Mailing email address"
        verbose_name_plural = "Mailing email addresses"
