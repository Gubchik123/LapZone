from django import forms
from django.contrib.auth.models import User

from general.forms import get_field_widget_attrs_with_placeholder_


class UserModelForm(forms.ModelForm):
    """Form for the User model."""

    def __init__(self, *args, **kwargs) -> None:
        """Initializes the UserModelForm."""
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = ""
        self.fields["first_name"].required = False
        self.fields["last_name"].required = False

    class Meta:
        """Meta options for the UserModelForm."""

        model = User
        fields = ["username", "first_name", "last_name"]
        widgets = {
            "username": forms.TextInput(
                attrs=get_field_widget_attrs_with_placeholder_("Username")
            ),
            "first_name": forms.TextInput(
                attrs=get_field_widget_attrs_with_placeholder_("First name")
            ),
            "last_name": forms.TextInput(
                attrs=get_field_widget_attrs_with_placeholder_("Last name")
            ),
        }
