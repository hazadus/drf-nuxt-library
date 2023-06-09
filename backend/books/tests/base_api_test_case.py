import json

from django.conf import settings

from rest_framework.test import APITestCase

from users.models import CustomUser


class BaseAPITest(APITestCase):
    """
    Base class for DRF API endpoint tests.
    """

    username = "testuser"
    password = "password"
    first_name = "Ivan"
    last_name = "Ivanov"
    new_user = None
    auth_token = None
    fixtures = ["books/tests/test_api_fixtures.json"]

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

    def test_debug_off(self):
        """
        We do not want to run tests with DEBUG mode on.
        """
        self.assertFalse(settings.DEBUG, msg="DEBUG mode should be off in tests!")
