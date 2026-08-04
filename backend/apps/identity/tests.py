from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.identity.models import User


class LoginAPITestCase(APITestCase):

    def setUp(self):
        self.password = "SecurePassword123!"

        self.user = User.objects.create_user(
            email="admin@atlas.com",
            password=self.password,
            first_name="Wilson",
            last_name="Mutinda",
        )

        self.url = reverse("login")

    def test_user_can_login_with_valid_credentials(self):
        data = {
            "email": "admin@atlas.com",
            "password": self.password,
        }

        response = self.client.post(
            self.url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["message"],
            "Login successful.",
        )

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        self.assertEqual(
            response.data["user"]["email"],
            self.user.email,
        )

    def test_login_fails_with_wrong_password(self):
        data = {
            "email": "admin@atlas.com",
            "password": "WrongPassword123!",
        }

        response = self.client.post(
            self.url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_login_fails_with_unknown_email(self):
        data = {
            "email": "unknown@atlas.com",
            "password": self.password,
        }

        response = self.client.post(
            self.url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_login_fails_when_password_is_missing(self):
        data = {
            "email": "admin@atlas.com",
        }

        response = self.client.post(
            self.url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

class CurrentUserAPITestCase(APITestCase):
    def setUp(self):
        self.password = "Atlas@123"

        self.user = User.objects.create_user(
            email="admin@atlas.com",
            password=self.password,
            first_name="wilson",
            last_name="mutinda",
        )

        self.url = reverse("current-user")

    def test_authenticated_user_can_get_profile(self):
        self.client.force_authenticate(
            user=self.user
        )
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["user"]["id"],
            self.user.id,
        )

        self.assertEqual(
            response.data["user"]["email"],
            self.user.email,
        )

        self.assertEqual(
            response.data["user"]["first_name"],
            self.user.first_name,
        )

        self.assertEqual(
            response.data["user"]["last_name"],
            self.user.last_name,
        )

    def test_unauthenticated_user_cannot_get_profile(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
