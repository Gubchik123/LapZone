from django.test import TestCase
from django.contrib.messages import get_messages
from django.core.validators import EmailValidator
from django.core.handlers.wsgi import WSGIRequest

from mailing.models import MailingEmailAddress
from mailing.forms import MailingEmailAddressModelForm
from general.test_mixins.for_views import ViewTestMixin, DeleteViewTestMixin


class MailingCreateViewTestCase(TestCase):
    """Tests for the MailingCreateView."""

    success_url = "/"
    url = "/mailing/create/"

    def test_form_valid(self):
        """Test that the form is valid if the email is valid."""
        self.assertTrue(
            MailingEmailAddressModelForm(
                {"email": "test@example.com"}
            ).is_valid()
        )

    def test_mailing_email_address_has_created(self):
        """Test that the mailing email address has successfully created."""
        response = self.client.post(
            self.url, {"email": "test@example.com"}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self._test_message_is_displayed(
            response.wsgi_request,
            "You have successfully subscribed to our mailing.",
        )
        self.assertTrue(
            MailingEmailAddress.objects.filter(
                email="test@example.com"
            ).exists()
        )

    def test_create_the_same_mailing_email_address(self):
        """
        Test that the same mailing email address has not successfully created.
        """
        self.test_mailing_email_address_has_created()
        response = self.client.post(
            self.url, {"email": "test@example.com"}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self._test_message_is_displayed(
            response.wsgi_request,
            "Mailing email address with this Email address already exists.",
        )

    def test_valid_redirect(self):
        """
        Test that the user is redirected to the success url if the form is valid.
        """
        response = self.client.post(self.url, {"email": "test@example.com"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.success_url)

    def test_form_invalid(self):
        """Test that the form is not invalid if the email is not invalid."""
        self.assertFalse(
            MailingEmailAddressModelForm({"email": "wrong-email@"}).is_valid()
        )

    def test_mailing_email_address_has_not_updated(self):
        """Test that the mailing email address has not successfully Created."""
        response = self.client.post(
            self.url, {"email": "wrong-email@"}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self._test_message_is_displayed(
            response.wsgi_request, EmailValidator.message
        )
        self.assertFalse(
            MailingEmailAddress.objects.filter(email="wrong-email@").exists()
        )

    def test_invalid_redirect(self):
        """
        Test that the user is redirected to the success url if the form is not valid.
        """
        response = self.client.post(self.url, {"email": "wrong-email@"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.success_url)

    def _test_message_is_displayed(
        self, wsgi_request: WSGIRequest, message: str
    ):
        """Test that the message is displayed."""
        messages = list(get_messages(wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, message)


class MailingDeleteViewTestCase(ViewTestMixin, DeleteViewTestMixin, TestCase):
    """Tests for the MailingDeleteView."""

    success_url = "/"
    name = "mailing:delete"
    is_login_required = False
    template_name = "mailing/confirm_delete.html"
    success_message = "You have successfully unsubscribed from our mailing."

    @classmethod
    def setUpTestData(cls) -> None:
        """Sets up test data by creating a mailing email address."""
        cls.mailing_email_address = MailingEmailAddress.objects.create(
            email="test@example.com"
        )
        cls.mailing_email_address_id = cls.mailing_email_address.id
        cls.url = f"/mailing/{cls.mailing_email_address_id}/delete/"
        cls.kwargs = {"pk": cls.mailing_email_address_id}

    def test_405_with_get_request(self):
        """Skips the test because there is GET handler in the view."""
        self.skipTest("There is GET handler in the MailingDeleteView.")

    def test_object_deleting(self):
        """Test that the mailing email address is deleted."""
        super().test_object_deleting()
        self.assertFalse(
            MailingEmailAddress.objects.filter(
                id=self.mailing_email_address_id
            ).exists()
        )

    def test_unsubscribe_btn_is_on_page(self):
        """Test that the unsubscribe button is on the page."""
        self.assertContains(self.response, "Unsubscribe")
