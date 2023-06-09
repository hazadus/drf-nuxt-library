#
# Tests for `authors/` endpoint.
# Tests tagged "noci" are excluded when running tests in GutHub Actions (because of missing media files).
#
import json

from django.test import tag as tag_test

from rest_framework import status

from books.models import Author

from .base_api_test_case import BaseAPITest


class AuthorsAPITest(BaseAPITest):
    """
    Test `authors/` DRF API endpoint.
    """

    @tag_test("noci")
    def test_authors_list_api(self):
        """
        Ensure that `AuthorListView`:

        - is located at expected URL;
        - return all authors in DB (not paginated);
        - data correctly serialized.
        """
        url = "/api/v1/authors/"
        response = self.client.get(
            url,
        )

        authors = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(authors), Author.objects.all().count())

        for author in authors:
            author_instance = Author.objects.get(pk=author["id"])
            self.assertEqual(author["id"], author_instance.pk)
            self.assertEqual(author["first_name"], author_instance.first_name)
            self.assertEqual(author["last_name"], author_instance.last_name)
            self.assertEqual(author["middle_name"], author_instance.middle_name)
            self.assertEqual(author["description"], author_instance.description)

            if author_instance.portrait:
                self.assertEqual(author["portrait"], author_instance.portrait.url)
                self.assertEqual(
                    author["portrait_thumbnail"], author_instance.portrait_thumbnail.url
                )

            # `user`:
            if author_instance.user:
                self.assertEqual(author["user"]["id"], author_instance.user.pk)
                self.assertEqual(
                    author["user"]["username"], author_instance.user.username
                )

                if author_instance.user.profile_image:
                    self.assertEqual(
                        author["user"]["profile_image"],
                        author_instance.user.profile_image.url,
                    )
                    self.assertEqual(
                        author["user"]["profile_image_thumbnail_small"],
                        author_instance.user.profile_image_thumbnail_small.url,
                    )
                    self.assertEqual(
                        author["user"]["profile_image_thumbnail_large"],
                        author_instance.user.profile_image_thumbnail_large.url,
                    )

    @tag_test("noci")
    def test_authors_list_with_query_api(self):
        """
        Ensure that `AuthorListView` with `?query=` parameter:

        - return correct list of authors (check by results count).
        """
        queries = [
            "мартин",
            "vincent",
            "сем",
        ]

        for query in queries:
            url = f"/api/v1/authors/?query={query}"
            response = self.client.get(
                url,
            )

            authors_filtered = Author.objects.filter(last_name__icontains=query)

            authors = json.loads(response.content)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(authors), authors_filtered.count())

    def test_authors_create_fails_without_auth_api(self):
        """
        Ensure that `AuthorCreateView` using POST method:

        - won't create Author instance without authentication, instead return `HTTP_401_UNAUTHORIZED`.
        """
        url = "/api/v1/authors/create/"
        response = self.client.post(
            url,
            {
                "last_name": "Ivanov",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authors_create_api(self):
        """
        Ensure that `AuthorCreateView` using POST method:

        - correctly creates Author instance;
        - auth'd user set as author (using `CreateAsAuthenticatedUser` mixin);
        - returns `HTTP_201_CREATED`;

        """
        url = "/api/v1/authors/create/"
        response = self.client.post(
            url,
            {
                "last_name": "Ivanov",
            },
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        author_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(author_data["user"], self.new_user.pk)
        self.assertEqual(author_data["last_name"], "Ivanov")

    @tag_test("noci")
    def test_authors_detail_api(self):
        """
        Ensure that `AuthorDetailView`:

        - return correct serialized author data with all expected fields.
        """
        authors = Author.objects.all()

        for author_instance in authors:
            url = f"/api/v1/authors/{author_instance.pk}/"
            response = self.client.get(
                url,
            )

            author = json.loads(response.content)
            self.assertEqual(author["id"], author_instance.pk)
            self.assertEqual(author["first_name"], author_instance.first_name)
            self.assertEqual(author["last_name"], author_instance.last_name)
            self.assertEqual(author["middle_name"], author_instance.middle_name)
            self.assertEqual(author["description"], author_instance.description)

            if author_instance.portrait:
                self.assertEqual(author["portrait"], author_instance.portrait.url)
                self.assertEqual(
                    author["portrait_thumbnail"], author_instance.portrait_thumbnail.url
                )

            # `user`:
            if author_instance.user:
                self.assertEqual(author["user"]["id"], author_instance.user.pk)
                self.assertEqual(
                    author["user"]["username"], author_instance.user.username
                )

                if author_instance.user.profile_image:
                    self.assertEqual(
                        author["user"]["profile_image"],
                        author_instance.user.profile_image.url,
                    )
                    self.assertEqual(
                        author["user"]["profile_image_thumbnail_small"],
                        author_instance.user.profile_image_thumbnail_small.url,
                    )
                    self.assertEqual(
                        author["user"]["profile_image_thumbnail_large"],
                        author_instance.user.profile_image_thumbnail_large.url,
                    )
