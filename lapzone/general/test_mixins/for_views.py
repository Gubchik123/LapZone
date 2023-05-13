from django.urls import reverse


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
