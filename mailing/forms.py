from django import forms

from .models import MailingEmailAddress


class MailingEmailAddressModelForm(forms.ModelForm):
    """Form for creating a mailing email address."""

    def clean_email(self):
        """Check if email is valid."""
        email = self.cleaned_data.get("email")

        if not email.endswith("@gmail.com"):
            raise forms.ValidationError("Please enter a Gmail email address.")
        return email

    class Meta:
        """Meta options for the MailingEmailAddressModelForm."""

        fields = ["email"]
        model = MailingEmailAddress
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email address"}
            )
        }   
 