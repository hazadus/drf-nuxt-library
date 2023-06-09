#
# Tests for `publishers/` endpoint.
# Tests tagged "noci" are excluded when running tests in GutHub Actions (because of missing media files).
#
import json

from rest_framework import status

from books.models import Publisher

from .base_api_test_case import BaseAPITest


class PublishersAPITest(BaseAPITest):
    """
    Test `publishers/` DRF API endpoint.
    """

    def test_publishers_list_api(self):
        """
        Ensure that `PublisherListView`:

        - is located at expected URL;
        - return all publishers in DB (not paginated);
        - data correctly serialized.
        """
        url = "/api/v1/publishers/"
        response = self.client.get(
            url,
        )

        all_publishers = Publisher.objects.all()

        publishers = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(publishers), all_publishers.count())

        for publisher in publishers:
            publisher_instance = Publisher.objects.get(pk=publisher["id"])
            self.assertEqual(publisher["id"], publisher_instance.pk)
            self.assertEqual(publisher["title"], publisher_instance.title)

    def test_publishers_list_with_query_api(self):
        """
        Ensure that `PublisherListView` with `?query=` parameter:

        - return correct list of publishers (check by results count).
        """
        queries = [
            "press",
            "pub",
        ]

        for query in queries:
            url = f"/api/v1/publishers/?query={query}"
            response = self.client.get(
                url,
            )

            publishers_filtered = Publisher.objects.filter(title__icontains=query)

            publishers = json.loads(response.content)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(publishers), publishers_filtered.count())

    def test_publishers_create_fails_without_auth_api(self):
        """
        Ensure that `PublisherListView` using POST method:

        - won't create Publisher instance without authentication, instead return `HTTP_401_UNAUTHORIZED`.
        """
        url = "/api/v1/publishers/"
        response = self.client.post(
            url,
            {
                "title": "Test Publisher",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_publishers_create_api(self):
        """
        Ensure that `PublisherListView` using POST method:

        - correctly creates Publisher instance;
        - auth'd user set as author (using `CreateAsAuthenticatedUser` mixin);
        - returns `HTTP_201_CREATED`;

        """
        url = "/api/v1/publishers/"
        publisher_title = "Test Publisher"
        response = self.client.post(
            url,
            {
                "title": publisher_title,
            },
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        publisher_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(publisher_data["user"], self.new_user.pk)
        self.assertEqual(publisher_data["title"], publisher_title)

    def test_publishers_detail_api(self):
        """
        Ensure that `PublisherDetailView`:

        - return correct serialized publisher data with all expected fields.
        """
        publishers = Publisher.objects.all()

        for publisher_instance in publishers:
            url = f"/api/v1/publishers/{publisher_instance.pk}/"
            response = self.client.get(
                url,
            )

            publisher_data = json.loads(response.content)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(publisher_data["id"], publisher_instance.pk)
            self.assertEqual(publisher_data["title"], publisher_instance.title)
            if publisher_instance.user:
                self.assertEqual(publisher_data["user"], publisher_instance.user.pk)
