from typing import NamedTuple

from django.views import View
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template.exceptions import TemplateDoesNotExist


class Error(NamedTuple):
    """Named tuple that holds information about an error."""

    code: int
    name: str
    description: str


class ErrorView(View):
    """Base error view for rendering the custom error page."""

    code: int
    name: str
    description: str

    def get(self, request: HttpRequest, exception=None) -> HttpResponse:
        """Returns the custom error page with the given error information."""
        try:
            return render(
                request,
                "pages/error.html",
                {"error": Error(self.code, self.name, self.description)},
                status=self.code,
            )
        except TemplateDoesNotExist:
            return HttpResponse(
                f"""
                <title>{self.code} | LapZone</title>
                <h1>{self.name}</h1>
                <h4>{self.description}</h4>
                """,
                status=self.code,
            )


class CustomBadRequestView(ErrorView):
    """Custom view for handling the 400 HTTP status code"""

    code = 400
    name = "Bad Request"
    description = "The server cannot or will not process the request."


class CustomPermissionDeniedView(ErrorView):
    """Custom view for handling the 403 HTTP status code"""

    code = 403
    name = "Permission denied"
    description = "You do not have access rights to the content."


class CustomNotFoundView(ErrorView):
    """Custom view for handling the 404 HTTP status code"""

    code = 404
    name = "Not Found"
    description = (
        "The server cannot find the requested resource. URL is not recognized."
    )


class CustomServerErrorView(ErrorView):
    """Custom view for handling the 500 HTTP status code"""

    code = 500
    name = "Internal Server Error"
    description = "Sorry, an error occurred in the server. Try again."
