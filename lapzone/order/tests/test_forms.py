from django import forms
from django.test import SimpleTestCase

from order.forms import OrderCheckoutModelForm
from general.forms import FIELD_WIDGET_ATTRS_CLASS
from customer.tests.test_forms import UserModelFormTestMixin


class OrderCheckoutModelFormSimpleTestCase(
    UserModelFormTestMixin, SimpleTestCase
):
    """Tests for the OrderCheckoutModelForm."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.form = OrderCheckoutModelForm()

    def test_form_fields(self):
        """Tests the form fields."""
        self.assertEqual(
            tuple(self.form.Meta.fields),
            (
                "is_create_profile",
                "username",
                "password",
                "first_name",
                "last_name",
                "phone_number",
                "email",
                "address",
                "order_comment",
            ),
        )

    # * --------- Testing the 'is_create_profile' field's parameters ---------

    def test_is_create_profile_field_label(self):
        """Tests the is_create_profile field label."""
        self.assertEqual(
            self.form.fields["is_create_profile"].label,
            "Create a profile automatically?",
        )

    def test_is_create_profile_field_choices(self):
        """Tests the is_create_profile field choices."""
        self.assertEqual(
            tuple(self.form.fields["is_create_profile"].choices),
            ((True, "Yes"), (False, "No")),
        )

    def test_is_create_profile_field_initial(self):
        """Tests the is_create_profile field initial value."""
        self.assertEqual(self.form.fields["is_create_profile"].initial, False)

    def test_is_create_profile_field_widget(self):
        """Tests the is_create_profile field widget."""
        self.assertIsInstance(
            self.form.fields["is_create_profile"].widget, forms.RadioSelect
        )

    # * ----------- Testing the 'phone_number' field's parameters ------------

    def test_phone_number_field_label(self):
        """Tests the phone_number field label."""
        self.assertEqual(
            self.form.fields["phone_number"].label, "Phone number"
        )

    def test_phone_number_field_max_length(self):
        """Tests the phone_number field max_length."""
        self.assertEqual(self.form.fields["phone_number"].max_length, 30)

    def test_phone_number_field_validators(self):
        """Tests the phone_number field validators."""
        self.assertEqual(
            self.form.fields["phone_number"].validators[0].regex.pattern,
            r"^\+?1?\d{9,15}$",
        )
        self.assertEqual(
            self.form.fields["phone_number"].validators[0].message,
            "Invalid phone number.",
        )

    def test_phone_number_field_widget(self):
        """Tests the phone_number field widget."""
        self.assertIsInstance(
            self.form.fields["phone_number"].widget, forms.TextInput
        )

    def test_phone_number_field_widget_attrs_class(self):
        """Tests the phone_number field widget attrs class."""
        self.assertEqual(
            self.form.fields["phone_number"].widget.attrs["class"],
            FIELD_WIDGET_ATTRS_CLASS,
        )

    def test_phone_number_field_widget_attrs_placeholder(self):
        """Tests the phone_number field widget attrs placeholder."""
        self.assertEqual(
            self.form.fields["phone_number"].widget.attrs["placeholder"],
            "+380501234567",
        )

    # * -------------- Testing the 'address' field's parameters --------------

    def test_address_field_label(self):
        """Tests the address field label."""
        self.assertEqual(self.form.fields["address"].label, "Address")

    def test_address_field_max_length(self):
        """Tests the address field max_length."""
        self.assertEqual(self.form.fields["address"].max_length, 255)

    def test_address_field_widget(self):
        """Tests the address field widget."""
        self.assertIsInstance(
            self.form.fields["address"].widget, forms.TextInput
        )

    def test_address_field_widget_attrs_class(self):
        """Tests the address field widget attrs class."""
        self.assertEqual(
            self.form.fields["address"].widget.attrs["class"],
            FIELD_WIDGET_ATTRS_CLASS,
        )

    def test_address_field_widget_attrs_placeholder(self):
        """Tests the address field widget attrs placeholder."""
        self.assertEqual(
            self.form.fields["address"].widget.attrs["placeholder"],
            "City, Street Name, House name / Flat number, Postcode",
        )

    # * ----------- Testing the 'order_comment' field's parameters -----------

    def test_order_comment_field_label(self):
        """Tests the order_comment field label."""
        self.assertEqual(
            self.form.fields["order_comment"].label, "Order comment (optional)"
        )

    def test_order_comment_field_max_length(self):
        """Tests the order_comment field max_length."""
        self.assertEqual(self.form.fields["order_comment"].max_length, 255)

    def test_order_comment_field_required(self):
        """Tests the order_comment field is not required."""
        self.assertFalse(self.form.fields["order_comment"].required)

    def test_order_comment_field_widget(self):
        """Tests the order_comment field widget."""
        self.assertIsInstance(
            self.form.fields["order_comment"].widget, forms.Textarea
        )

    def test_order_comment_field_widget_attrs_class(self):
        """Tests the order_comment field widget attrs class."""
        self.assertEqual(
            self.form.fields["order_comment"].widget.attrs["class"],
            FIELD_WIDGET_ATTRS_CLASS,
        )

    def test_order_comment_field_widget_attrs_placeholder(self):
        """Tests the order_comment field widget attrs placeholder."""
        self.assertEqual(
            self.form.fields["order_comment"].widget.attrs["placeholder"],
            "Optional comment to seller",
        )

    # * --------------- Testing the 'username' is not required ---------------

    def test_username_field_required(self):
        """Tests the username field is not required."""
        self.assertFalse(self.form.fields["username"].required)

    # * -------------- Testing the 'password' field's parameters -------------

    def test_password_field_required(self):
        """Tests the password field is not required."""
        self.assertFalse(self.form.fields["password"].required)

    def test_password_field_label(self):
        """Tests the password field label."""
        self.assertEqual(self.form.fields["password"].label, "Password")

    def test_password_field_widget(self):
        """Tests the password field widget."""
        self.assertIsInstance(
            self.form.fields["password"].widget, forms.PasswordInput
        )

    def test_password_field_widget_attrs_class(self):
        """Tests the password field widget attrs class."""
        self.assertEqual(
            self.form.fields["password"].widget.attrs["class"],
            FIELD_WIDGET_ATTRS_CLASS,
        )

    def test_password_field_widget_attrs_placeholder(self):
        """Tests the password field widget attrs placeholder."""
        self.assertEqual(
            self.form.fields["password"].widget.attrs["placeholder"],
            "Password",
        )

    # * --------------- Testing the 'email' field's parameters ---------------

    def test_email_field_required(self):
        """Tests the email field is required."""
        self.assertTrue(self.form.fields["email"].required)

    def test_email_field_label(self):
        """Tests the email field label."""
        self.assertEqual(self.form.fields["email"].label, "Email address")

    def test_email_field_widget(self):
        """Tests the email field widget."""
        self.assertIsInstance(
            self.form.fields["email"].widget, forms.EmailInput
        )

    def test_email_field_widget_attrs_class(self):
        """Tests the email field widget attrs class."""
        self.assertEqual(
            self.form.fields["email"].widget.attrs["class"],
            FIELD_WIDGET_ATTRS_CLASS,
        )

    def test_email_field_widget_attrs_placeholder(self):
        """Tests the email field widget attrs placeholder."""
        self.assertEqual(
            self.form.fields["email"].widget.attrs["placeholder"],
            "Where should we send the receipt?",
        )

    # * ---------------- Testing the 'first_name' is required ----------------

    def test_first_name_field_required(self):
        """Tests the first_name field is required."""
        self.assertTrue(self.form.fields["first_name"].required)

    # * ---------------- Testing the 'last_name' is required -----------------

    def test_last_name_field_required(self):
        """Tests the last_name field is required."""
        self.assertTrue(self.form.fields["last_name"].required)
