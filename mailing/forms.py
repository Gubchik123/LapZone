from django import forms

from .models import MailingEmailAddress


class MailingEmailAddressModelForm(forms.ModelForm):
    """Form for creating a mailing email address."""

    class Meta:
        """Meta options for the MailingEmailAddressModelForm."""

        fields = ["email"]
        model = MailingEmailAddress
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email address"}
            )
        }
