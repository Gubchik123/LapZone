from django.views import generic
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from . import services
from general.views import BaseView
from .forms import MailingEmailAddressModelForm


class MailingCreateView(BaseView, generic.View):
    """View for creating a mailing email address."""

    def post(self, request: HttpRequest) -> HttpResponse:
        """Handles the POST request
        and returns a redirect to the URL from which the request was made."""
        form = MailingEmailAddressModelForm(request.POST)

        if form.is_valid():
            mailing_user = form.save()
            services.send_mail_to_(mailing_user.email)
            messages.success(
                self.request,
                "You have successfully subscribed to our mailing.",
            )
        else:
            for error in form.errors.as_data().values():
                messages.warning(self.request, error[0].messages[0])
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
