import json

from rest_framework.test import APITestCase

from users.models import CustomUser


class UsersAPITest(APITestCase):
    """
    Test `users` app DRF API.
    """

    username = "testuser"
    password = "password"
    first_name = "Ivan"
    last_name = "Ivanov"
    new_user = None
    auth_token = None

    @classmethod
    def setUpTestData(cls):
        cls.new_user = CustomUser.objects.create_user(
            cls.username,
            password=cls.password,
            first_name=cls.first_name,
            last_name=cls.last_name,
        )

    def setUp(self):
        """
        Login to get auth token for further tests.
        """
        url = "/api/v1/token/login/"
        response = self.client.post(
            url,
            {"username": self.username, "password": self.password},
        )
        self.auth_token = json.loads(response.content).get("auth_token")

    def test_logged_in_user_detail_api(self):
        """
        Ensure that `AuthenticatedUserDetailView`:
        - is located at defined URL;
        - returns basic necessary data.
        """
        url = "/api/v1/user/details/"
        response = self.client.get(
            url,
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        user_details = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user_details["username"], self.username)
        self.assertEqual(user_details["first_name"], self.first_name)
        self.assertEqual(user_details["last_name"], self.last_name)

    def test_logged_in_user_detail_api_fails_without_auth(self):
        """
        Ensure that `AuthenticatedUserDetailView`:
        - return 401 error if user is not authorized
        """
        url = "/api/v1/user/details/"
        response = self.client.get(
            url,
        )

        self.assertEqual(response.status_code, 401)
