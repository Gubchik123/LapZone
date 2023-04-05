from django.urls import reverse


class ViewURLTestMixin:
    """Test mixin to test a view's URL and template."""

    url: str
    template_name: str

    def setUp(self) -> None:
        """Sets up the test by retrieving a response from the view's URL."""
        self.response = self.client.get(self.url)

    def test_view_url_exists_at_desired_location(self):
        """Test that the view exists at desired location."""
        self.assertEqual(self.response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test that the response in the view uses the correct template."""
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, self.template_name)


class ViewNameTestMixin:
    """Test mixin to test a view's path name."""

    name: str
    kwargs = {}

    def test_view_url_accessible_by_name(self):
        """Test that the view is accessible using its name."""
        response = self.client.get(reverse(self.name, kwargs=self.kwargs))
        self.assertEqual(response.status_code, 200)


class ViewTestMixin(ViewURLTestMixin, ViewNameTestMixin):
    """Base test mixin for views."""
