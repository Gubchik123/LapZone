import logging

from django import http
from django.contrib import messages
from django.core.exceptions import BadRequest, PermissionDenied

from general.error_views import Error, CustomServerErrorView, render_error_page

logger = logging.getLogger(__name__)


class BaseView:
    """Base view for all other views with exception handling."""

    def dispatch(
            self, request: http.HttpRequest, *args, **kwargs
    ) -> http.HttpResponse:
        """Handles exceptions during dispatch and returns a response."""
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            exception_type = type(e)

            # Check if it's an exception for which there is an error handler.
            if exception_type in (http.Http404, BadRequest, PermissionDenied):
                raise e

            logger.error(
                f"{exception_type}('{str(e)}') during working with {request.path} URL"
            )

            error_view = CustomServerErrorView
            return render_error_page(
                request,
                Error(
                    error_view.code, error_view.name, error_view.description
                ),
            )


class DeleteViewMixin:
    """Mixin for DeleteViews which handles POST requests."""

    success_message: str
    http_method_names = ["post"]

    def post(
            self, request: http.HttpRequest, *args, **kwargs
    ) -> http.HttpResponseRedirect:
        """Adds the success_message and calls the super method."""
        messages.success(request, self.success_message)
        return super().post(request, *args, **kwargs)
