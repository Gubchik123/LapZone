from django.urls import reverse
from django.contrib.messages import get_messages


class _ViewTestMixin:
    """Base test mixin for view test mixins."""

    is_login_required = False

    def _login_if_it_is_required(self):
        """Logs in the user."""
        if self.is_login_required:
            self.assertTrue(
                self.client.login(username="testuser", password="testpass")
            )


class ViewURLTestMixin(_ViewTestMixin):
    """Test mixin to test a view's URL and template."""

    url: str
    template_name: str

    def setUp(self) -> None:
        """Sets up the test by retrieving a response from the view's URL."""
        self._login_if_it_is_required()
        self.response = self.client.get(self.url)

    def test_view_url_exists_at_desired_location(self):
        """Test that the view exists at desired location."""
        self.assertEqual(self.response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test that the response in the view uses the correct template."""
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, self.template_name)


class ViewNameTestMixin(_ViewTestMixin):
    """Test mixin to test a view's path name."""

    name: str
    kwargs = {}

    def test_view_url_accessible_by_name(self):
        """Test that the view is accessible using its name."""
        self._login_if_it_is_required()
        response = self.client.get(reverse(self.name, kwargs=self.kwargs))
        self.assertEqual(response.status_code, 200)


class ViewTestMixin(ViewURLTestMixin, ViewNameTestMixin):
    """Base test mixin for views."""


class LoginRequiredTestMixin:
    """Test mixin for testing login required views."""

    def test_302_status_code_if_user_is_not_authenticated(self):
        """
        Test that the 302 status code is returned if the user is not authenticated.
        """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_login_required_redirect_url_if_user_is_not_authenticated(self):
        """
        Test that the user is redirected to the login page if not authenticated.
        """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(
            response.url,
            f"{reverse('account_login')}?next={self.url}",
        )


class DeleteViewTestMixin:
    """Test mixin for testing views that inherit from the DeleteView."""

    success_url: str
    success_message: str

    def test_405_with_get_request(self):
        """Test that GET request returns 405 status code."""
        self._login()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_object_deleting(self):
        """Test that the object is deleted."""
        self._login()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_success_message(self):
        """Test that a success message is added to messages framework."""
        self._login()
        response = self.client.post(self.url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, self.success_message)

    def test_redirects_to_success_url(self):
        """Test redirects to the success URL."""
        self._login()
        response = self.client.post(self.url)
        self.assertRedirects(response, self.success_url)

    def _login(self):
        """Logs in the first user."""
        self.assertTrue(
            self.client.login(username="testuser", password="testpass")
        )
