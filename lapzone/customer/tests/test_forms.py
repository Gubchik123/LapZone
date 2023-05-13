from django import forms
from django.test import SimpleTestCase
from django.contrib.auth.models import User

from customer.forms import UserModelForm
from general.forms import FIELD_WIDGET_ATTRS_CLASS


class UserModelFormTestMixin:
    """Mixin for testing the UserModelForm and its subclasses."""

    def test_form_model(self):
        """Tests the form model."""
        self.assertEqual(self.form.Meta.model, User)

    # * -------------- Testing the 'username' field's parameters -------------

    def test_username_field_help_text(self):
        """Tests the username field help_text."""
        self.assertEqual(self.form.fields["username"].help_text, "")

    def test_username_field_label(self):
        """Tests the username field label."""
        self.assertEqual(self.form.fields["username"].label, "Username")

    def test_username_field_widget(self):
        """Tests the username field widget."""
        self.assertIsInstance(
            self.form.fields["username"].widget, forms.TextInput
        )

    def test_username_field_widget_attrs_class(self):
        """Tests the username field widget attrs class."""
        self.assertEqual(
            self.form.fields["username"].widget.attrs["class"],
            FIELD_WIDGET_ATTRS_CLASS,
        )

    def test_username_field_widget_attrs_placeholder(self):
        """Tests the username field widget attrs placeholder."""
        self.assertEqual(
            self.form.fields["username"].widget.attrs["placeholder"],
            "Username",
        )

    # * ------------- Testing the 'first_name' field's parameters ------------

    def test_first_name_field_label(self):
        """Tests the first_name field label."""
        self.assertEqual(self.form.fields["first_name"].label, "First name")

    def test_first_name_field_widget(self):
        """Tests the first_name field widget."""
        self.assertIsInstance(
            self.form.fields["first_name"].widget, forms.TextInput
        )

    def test_first_name_field_widget_attrs_class(self):
        """Tests the first_name field widget attrs class."""
        self.assertEqual(
            self.form.fields["first_name"].widget.attrs["class"],
            FIELD_WIDGET_ATTRS_CLASS,
        )

    def test_first_name_field_widget_attrs_placeholder(self):
        """Tests the first_name field widget attrs placeholder."""
        self.assertEqual(
            self.form.fields["first_name"].widget.attrs["placeholder"],
            "First name",
        )

    # * ------------- Testing the 'last_name' field's parameters -------------

    def test_last_name_field_label(self):
        """Tests the last_name field label."""
        self.assertEqual(self.form.fields["last_name"].label, "Last name")

    def test_last_name_field_widget(self):
        """Tests the last_name field widget."""
        self.assertIsInstance(
            self.form.fields["last_name"].widget, forms.TextInput
        )

    def test_last_name_field_widget_attrs_class(self):
        """Tests the last_name field widget attrs class."""
        self.assertEqual(
            self.form.fields["last_name"].widget.attrs["class"],
            FIELD_WIDGET_ATTRS_CLASS,
        )

    def test_last_name_field_widget_attrs_placeholder(self):
        """Tests the last_name field widget attrs placeholder."""
        self.assertEqual(
            self.form.fields["last_name"].widget.attrs["placeholder"],
            "Last name",
        )


class UserModelFormSimpleTestCase(UserModelFormTestMixin, SimpleTestCase):
    """Tests for the UserModelForm."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.form = UserModelForm()

    def test_form_fields(self):
        """Tests the form fields."""
        self.assertEqual(
            tuple(self.form.Meta.fields),
            ("username", "first_name", "last_name"),
        )

    def test_first_name_field_required(self):
        """Tests the first_name field is not required."""
        self.assertFalse(self.form.fields["first_name"].required)

    def test_last_name_field_required(self):
        """Tests the last_name field is not required."""
        self.assertFalse(self.form.fields["last_name"].required)
