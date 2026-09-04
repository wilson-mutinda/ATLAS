from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

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

class TokenRefreshAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="admin@atlas.com",
            password="Atlas@123",
            first_name="wilson",
            last_name="mutinda",
        )

        self.url = reverse("token-refresh")

        self.refresh_token = str(
            RefreshToken.for_user(self.user)
        )

    def test_user_can_refresh_access_token(self):
        data = {
            "refresh": self.refresh_token,
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

        self.assertIn(
            "access",
            response.data,
        )

    def test_refresh_fails_with_invalid_token(self):
        data = {
            "refresh": "invalid-token",
        }

        response = self.client.post(
            self.url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

class LogoutAPITestCase(APITestCase):
    def setUp(self):
        self.password = 'Atlas@123'

        self.user = User.objects.create_user(
            email='admin@atlas.com',
            password=self.password,
            first_name="wilson",
            last_name="mutinda",
        )

        self.login_url = reverse("login")
        self.logout_url = reverse("logout")

        login_response = self.client.post(
            self.login_url,
            {
                "email": "admin@atlas.com",
                "password": self.password,
            },
            format="json",
        )

        self.access_token = login_response.data["access"]
        self.refresh_token = login_response.data["refresh"]

    def test_authenticated_user_can_logout(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        response = self.client.post(
            self.logout_url,
            {
                "refresh": self.refresh_token,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["message"],
            "Logout successful.",
        )

    def test_logout_fails_with_invalid_refresh_token(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        response = self.client.post(
            self.logout_url,
            {
                "refresh": "invalid-token",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_logout_requires_authentication(self):
        response = self.client.post(
            self.logout_url,
            {
                "refresh": self.refresh_token,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

class ChangePasswordAPITestCase(APITestCase):

    def setUp(self):
        self.password = "user1234"

        self.user = User.objects.create_user(
            email="admin@atlas.com",
            password=self.password,
            first_name="wilson",
            last_name="mutinda",
        )

        self.login_url = reverse("login")
        self.change_password_url = reverse("password-change")

        login_response = self.client.post(
            self.login_url,
            {
                "email": "admin@atlas.com",
                "password": self.password,
            },
            format="json",
        )

        self.access_token = login_response.data["access"]

    def test_authenticated_user_can_change_password(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        response = self.client.post(
            self.change_password_url,
            {
                "current_password": self.password,
                "new_password": "user12345",
                "new_password_confirm": "user12345",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["message"],
            "Password changed successfully.",
        )

    def test_change_password_requires_authentication(self):
        response = self.client.post(
            self.change_password_url,
            {
                "current_password": self.password,
                "new_password": "user12345",
                "new_password_Confirm": "user12345",
            },
            format="json",
        )  

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_change_password_rejects_wrong_current_password(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )  

        response = self.client.post(
            self.change_password_url,
            {
                "current_password": "user12345",
                "new_password": "user1234",
                "new_password_confirm": "user1234",
            },
            format="json",
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_change_password_rejects_mismatched_passwords(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        response = self.client.post(
            self.change_password_url,
            {
                "current_password": self.password,
                "new_password": "user12345",
                "new_password_confirm": "user1234",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
