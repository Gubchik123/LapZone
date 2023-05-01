from django import forms
from django.core.validators import RegexValidator


def _get_field_widget_attrs_with_placeholder_(
    placeholder: str,
) -> dict[str, str]:
    """Returns a dict of field widget attributes with the given placeholder."""
    return {"class": "w-50 form-control mb-2", "placeholder": placeholder}


class OrderCreateForm(forms.Form):
    """Form for creating an order."""

    is_create_profile = forms.ChoiceField(
        label="Create a profile automatically?",
        choices=((True, "Yes"), (False, "No")),
        initial=False,
        widget=forms.RadioSelect,
    )
    first_name = forms.CharField(
        label="First name",
        min_length=2,
        max_length=30,
        widget=forms.TextInput(
            attrs=_get_field_widget_attrs_with_placeholder_("First name")
        ),
    )
    last_name = forms.CharField(
        label="Last name",
        min_length=2,
        max_length=30,
        widget=forms.TextInput(
            attrs=_get_field_widget_attrs_with_placeholder_("Last name")
        ),
    )
    phone_number = forms.CharField(
        label="Phone number",
        max_length=30,
        validators=[
            RegexValidator(r"^\+?1?\d{9,15}$", "Invalid phone number.")
        ],
        widget=forms.TextInput(
            attrs=_get_field_widget_attrs_with_placeholder_("+380501234567")
        ),
    )
    email = forms.EmailField(
        label="Email",
        max_length=255,
        widget=forms.EmailInput(
            attrs=_get_field_widget_attrs_with_placeholder_(
                "Where should we send your receipt?"
            )
        ),
    )
    address = forms.CharField(
        label="Address",
        max_length=255,
        widget=forms.TextInput(
            attrs=_get_field_widget_attrs_with_placeholder_(
                "Address (apartment, suite, unit, building, floor)"
            )
        ),
    )
    postal_code = forms.IntegerField(
        label="Postal code",
        min_value=0,
        max_value=99999,
        widget=forms.NumberInput(
            attrs=_get_field_widget_attrs_with_placeholder_("Zip/Postal code")
        ),
    )
    order_comment = forms.CharField(
        label="Order comment (optional)",
        max_length=255,
        required=False,
        widget=forms.Textarea(
            attrs=_get_field_widget_attrs_with_placeholder_(
                "Optional comment to seller"
            )
        ),
    )
