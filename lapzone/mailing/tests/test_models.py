from django.test import SimpleTestCase

from mailing.models import MailingEmailAddress
from general.test_mixins.for_models import (
    ModelWithUUIDPKTestMixin,
    ModelWithCreatedDateTimeTestMixin,
)


class MailingEmailAddressSimpleTestCase(
    ModelWithUUIDPKTestMixin, ModelWithCreatedDateTimeTestMixin, SimpleTestCase
):
    """Tests for the MailingEmailAddress model."""

    model = MailingEmailAddress

    def test_email_verbose_name(self):
        """Test that the email field's verbose name is "Email address"."""
        self.assertEqual(
            self.model._meta.get_field("email").verbose_name, "Email address"
        )

    def test_email_unique(self):
        """Test that the email field is unique."""
        self.assertTrue(self.model._meta.get_field("email").unique)

    def test_email_blank(self):
        """Test that the email field is not blank."""
        self.assertFalse(self.model._meta.get_field("email").blank)

    def test_email_null(self):
        """Test that the email field is not null."""
        self.assertFalse(self.model._meta.get_field("email").null)
