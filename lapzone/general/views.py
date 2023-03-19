import logging

from django.views import View
from django.http import HttpRequest, HttpResponse, Http404
from django.core.exceptions import BadRequest, PermissionDenied

from general.error_views import Error, CustomServerErrorView, render_error_page


logger = logging.getLogger(__name__)


class BaseView(View):
    """Base view for all other views with exception handling"""

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Handles exceptions during dispatch and returns a response"""
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            # Check if it's an exception for which there is an error handler.
            if type(e) in (Http404, BadRequest, PermissionDenied):
                raise e

            logger.error(f"{str(e)} during working with {request.path} URL")

            server_error = CustomServerErrorView
            return render_error_page(
                request,
                Error(
                    server_error.code,
                    server_error.name,
                    server_error.description,
                ),
            )
