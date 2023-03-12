import logging

from django.views import View
from django.http import HttpRequest, HttpResponse

from general.error_views import CustomServerErrorView


logger = logging.getLogger(__name__)


class BaseView(CustomServerErrorView, View):
    """Base view for all other views with exception handling"""

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Handles exceptions during dispatch and returns a response"""
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"{str(e)} during working with {request.path} URL")

            # Returns the error page of CustomServerErrorView
            return super().get(request)
