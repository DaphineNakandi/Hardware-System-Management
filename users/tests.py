from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class LoginViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testmanager",
            password="Strong-test-password-123",
            is_superuser=True,
        )

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "username")

    def test_valid_superuser_login_redirects_to_dashboard(self):
        response = self.client.post(
            reverse("login"),
            {"username": "testmanager", "password": "Strong-test-password-123"},
        )
        self.assertRedirects(response, reverse("dashboard"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_invalid_login_shows_error(self):
        response = self.client.post(
            reverse("login"),
            {"username": "testmanager", "password": "incorrect-password"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password.")
        self.assertFalse(response.wsgi_request.user.is_authenticated)
