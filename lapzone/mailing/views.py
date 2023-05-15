from django.views import generic
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from . import services
from .models import MailingEmailAddress
from .forms import MailingEmailAddressModelForm
from general.views import BaseView, DeleteViewMixin


class MailingCreateView(BaseView, generic.View):
    """View for creating a mailing email address."""

    def post(self, request: HttpRequest) -> HttpResponse:
        """Handles the POST request
        and returns a redirect to the URL from which the request was made."""
        form = MailingEmailAddressModelForm(request.POST)

        if form.is_valid():
            services.send_mail_to_(
                mailing_email_address=form.save(), request=request
            )
            messages.success(
                request, "You have successfully subscribed to our mailing."
            )
        else:
            for error in form.errors.as_data().values():
                messages.warning(request, error[0].messages[0])
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


class MailingDeleteView(BaseView, DeleteViewMixin, generic.DeleteView):
    """View for deleting a mailing email address."""

    success_url = "/"
    model = MailingEmailAddress
    http_method_names = ["get", "post"]
    template_name = "mailing/confirm_delete.html"
    success_message = "You have successfully unsubscribed from our mailing."
