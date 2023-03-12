from typing import NoReturn

from django.urls import path
from django.views import View
from django.test import SimpleTestCase
from django.http import HttpRequest, HttpResponse, Http404
from django.core.exceptions import PermissionDenied, BadRequest

from general.error_views import (
    ErrorView,
    CustomBadRequestView,
    CustomPermissionDeniedView,
    CustomNotFoundView,
    CustomServerErrorView,
)
from general.views import BaseView
from lapzone.urls import urlpatterns, handler400, handler403, handler404


class RaiseExceptionView(View):
    """View that raises the exception attribute."""

    exception: Exception

    def get(self, request: HttpRequest) -> NoReturn:
        """Raises the specified exception."""
        raise self.exception


class BadRequestView(RaiseExceptionView):
    """View that raises a 400 Bad Request exception."""

    exception = BadRequest


class PermissionDeniedView(RaiseExceptionView):
    """View that raises a 403 Permission Denied exception."""

    exception = PermissionDenied


class NotFoundView(RaiseExceptionView):
    """View that raises a 404 Not Found exception."""

    exception = Http404


class ServerErrorView(BaseView):
    """View that has error"""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Has error before returns response"""
        print(1 / 0)  # ZeroDivisionError
        return HttpResponse("Some content")


# Adding URLs for testing custom error handlers.
# Because the custom error page extends _base.html,
# where there are some links by view names such as "faq" and "about".
urlpatterns += [
    path("400/", BadRequestView.as_view()),
    path("403/", PermissionDeniedView.as_view()),
    path("404/", NotFoundView.as_view()),
    path("500/", ServerErrorView.as_view()),
]


class CustomErrorHandlerTestMixin:
    """Test mixin for custom error handlers."""

    error_handler: ErrorView

    def setUp(self):
        """Gets response with test client by generated url attribute"""
        self.response = self.client.get(f"/{self.error_handler.code}/")

    def test_view_status_code(self):
        """Asserts response status code matches code attribute"""
        self.assertEqual(self.response.status_code, self.error_handler.code)

    def test_view_template(self):
        """Asserts response template matches template_name attribute"""
        self.assertTemplateUsed(self.response, "pages/error.html")

    def test_view_content(self):
        """Asserts response content"""
        self.assertContains(
            self.response,
            self.error_handler.name,
            status_code=self.error_handler.code,
        )
        self.assertContains(
            self.response,
            self.error_handler.description,
            status_code=self.error_handler.code,
        )


class CustomBadRequestViewTest(CustomErrorHandlerTestMixin, SimpleTestCase):
    """Tests for CustomBadRequestView"""

    error_handler = CustomBadRequestView


class CustomForbiddenViewTest(CustomErrorHandlerTestMixin, SimpleTestCase):
    """Tests for CustomPermissionDeniedView"""

    error_handler = CustomPermissionDeniedView


class CustomNotFoundViewTest(CustomErrorHandlerTestMixin, SimpleTestCase):
    """Tests for CustomNotFoundView"""

    error_handler = CustomNotFoundView


class CustomServerErrorViewTest(CustomErrorHandlerTestMixin, SimpleTestCase):
    """Tests for CustomServerErrorView"""

    error_handler = CustomServerErrorView
