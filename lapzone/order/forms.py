from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from general.forms import get_field_widget_attrs_with_placeholder_


class OrderCheckoutModelForm(forms.ModelForm):
    """Form for checking out an order."""

    is_create_profile = forms.ChoiceField(
        label="Create a profile automatically?",
        choices=((True, "Yes"), (False, "No")),
        initial=False,
        widget=forms.RadioSelect,
    )
    phone_number = forms.CharField(
        label="Phone number",
        max_length=30,
        validators=[
            RegexValidator(r"^\+?1?\d{9,15}$", "Invalid phone number.")
        ],
        widget=forms.TextInput(
            attrs=get_field_widget_attrs_with_placeholder_("+380501234567")
        ),
    )
    address = forms.CharField(
        label="Address",
        max_length=255,
        widget=forms.TextInput(
            attrs=get_field_widget_attrs_with_placeholder_(
                "City, Street Name, House name / Flat number, Postcode"
            )
        ),
    )
    order_comment = forms.CharField(
        label="Order comment (optional)",
        max_length=255,
        required=False,
        widget=forms.Textarea(
            attrs=get_field_widget_attrs_with_placeholder_(
                "Optional comment to seller"
            )
        ),
    )

    def __init__(self, *args, **kwargs):
        """Initializes the OrderCheckoutModelForm."""
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = ""
        self.fields["username"].required = False
        self.fields["password"].required = False

        self.fields["email"].required = True
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True

    class Meta:
        """Meta options for the OrderCreateModelForm."""

        model = User
        fields = (
            "is_create_profile",
            "username",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "address",
            "order_comment",
        )
        widgets = {
            "username": forms.TextInput(
                attrs=get_field_widget_attrs_with_placeholder_("Username")
            ),
            "password": forms.PasswordInput(
                attrs=get_field_widget_attrs_with_placeholder_("Password")
            ),
            "email": forms.EmailInput(
                attrs=get_field_widget_attrs_with_placeholder_(
                    "Where should we send the receipt?"
                )
            ),
            "first_name": forms.TextInput(
                attrs=get_field_widget_attrs_with_placeholder_("First name")
            ),
            "last_name": forms.TextInput(
                attrs=get_field_widget_attrs_with_placeholder_("Last name")
            ),
        }
