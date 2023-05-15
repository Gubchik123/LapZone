from django import forms
from django.test import SimpleTestCase

from mailing.models import MailingEmailAddress
from mailing.forms import MailingEmailAddressModelForm


class MailingEmailAddressModelFormSimpleTestCase(SimpleTestCase):
    """Tests for the MailingEmailAddressModelForm."""

    @classmethod
    def setUpClass(cls) -> None:
        """Sets up the form for testing."""
        super().setUpClass()
        cls.form = MailingEmailAddressModelForm()

    # * ------------------- Testing the form Meta options --------------------

    def test_form_fields(self):
        """Tests the form fields."""
        self.assertEqual(list(self.form.Meta.fields), ["email"])

    def test_form_model(self):
        """Tests the form model."""
        self.assertEqual(self.form.Meta.model, MailingEmailAddress)

    # * --------------- Testing the 'email' field's widget -------------------

    def test_email_field_widget(self):
        """Tests the email field widget."""
        self.assertIsInstance(
            self.form.fields["email"].widget, forms.EmailInput
        )

    def test_email_field_widget_attrs_class(self):
        """Tests the email field widget attrs class."""
        self.assertEqual(
            self.form.fields["email"].widget.attrs["class"], "form-control"
        )

    def test_email_field_widget_attrs_placeholder(self):
        """Tests the email field widget attrs placeholder."""
        self.assertEqual(
            self.form.fields["email"].widget.attrs["placeholder"],
            "Email address",
        )
