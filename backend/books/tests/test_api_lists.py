#
# Tests for `lists/` endpoint.
# Tests tagged "noci" are excluded when running tests in GutHub Actions (because of missing media files).
#
import json

from django.db.models import Q
from django.test import tag as tag_test
from rest_framework import status

from books.models import List

from .base_api_test_case import BaseAPITest

NUMBER_OF_PRIVATE_LISTS = 5


class ListsAPITest(BaseAPITest):
    """
    Test `lists/` DRF API endpoint.
    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        for i in range(0, NUMBER_OF_PRIVATE_LISTS):
            List.objects.create(
                user=cls.new_user,
                title=f"Test private list #{i}",
                description=f"Description for test private list #{i} of {cls.new_user.username}",
                is_public=False,
            )

    @tag_test("noci")
    def test_lists_list_without_auth_api(self):
        """
        Ensure that `ListListView`:

        - return `HTTP_200_OK` without authentication;
        - return only all public Lists without authentication;
        - List data is properly serialized.
        """
        url = "/api/v1/lists/"
        response = self.client.get(
            url,
        )

        public_lists = List.objects.filter(is_public=True)
        lists = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(lists),
            public_lists.count(),
        )

        for list_data in lists:
            list_instance = List.objects.get(pk=list_data["id"])
            self.check_list_serialized_data(list_data, list_instance)

    @tag_test("noci")
    def test_lists_list_without_auth_with_bookid_api(self):
        """
        Ensure that `ListListView` without auth, with `?book_id=...`:

        - return `HTTP_200_OK`;
        - return correct public lists with this book included.
        """
        url = f"/api/v1/lists/?book_id={1}"
        response = self.client.get(
            url,
        )

        list_instances = List.objects.filter(items__book_id__exact=1, is_public=True)
        lists = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(lists),
            list_instances.count(),
        )

    @tag_test("noci")
    def test_lists_list_with_auth_api(self):
        """
        Ensure that `ListListView`:

        - return `HTTP_200_OK` with authentication;
        - return all public Lists and private lists of authenticated user.
        """
        url = "/api/v1/lists/"
        response = self.client.get(
            url,
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        public_and_users_lists = List.objects.filter(
            Q(is_public=True) | (Q(user=self.new_user) & Q(is_public=False)),
        )
        lists = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(lists),
            public_and_users_lists.count(),
        )

        for list_data in lists:
            list_instance = List.objects.get(pk=list_data["id"])
            self.check_list_serialized_data(list_data, list_instance)

    @tag_test("noci")
    def test_lists_list_with_auth_with_bookid_api(self):
        """
        Ensure that `ListListView` with auth, with `?book_id=...`:

        - return `HTTP_200_OK`;
        - return correct public and user's lists with this book included.
        """
        book_id = 1
        url = f"/api/v1/lists/?book_id={book_id}"
        response = self.client.get(
            url,
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        list_instances = List.objects.filter(
            Q(is_public=True) | Q(user_id=self.new_user.pk)
        )
        list_instances = list_instances.filter(
            items__book_id__in=[
                book_id,
            ]
        )
        lists = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(lists),
            list_instances.count(),
        )

    @tag_test("noci")
    def test_lists_list_with_auth_with_only_own_lists_api(self):
        """
        Ensure that `ListListView` with auth, with `?only_own_lists=true`:

        - return `HTTP_200_OK`;
        - return correct public and private user's lists (check bo count).
        """
        url = "/api/v1/lists/?only_own_lists=true"
        response = self.client.get(
            url,
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        list_instances = List.objects.filter(user_id=self.new_user.pk)
        lists = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(lists),
            list_instances.count(),
        )

    @tag_test("noci")
    def test_lists_detail_public_without_auth_api(self):
        """
        Ensure that `ListDetailView` for public Lists without auth:

        - return `HTTP_200_OK`;
        - return detailed data for each public list, properly serialized.
        """

        public_lists = List.objects.filter(is_public=True)

        for list_instance in public_lists:
            url = f"/api/v1/lists/{list_instance.pk}/"
            response = self.client.get(
                url,
            )
            list_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.check_detail_serialized_data(list_data, list_instance)

    def test_lists_detail_fails_for_others_private_list_without_auth_api(self):
        """
        Ensure that `ListDetailView`:

        - return `HTTP_403_FORBIDDEN` when trying to access other's private list, without auth.
        """
        others_private_list = List.objects.filter(
            user_id=1,
            is_public=False,
        ).first()

        url = f"/api/v1/lists/{others_private_list.pk}/"
        response = self.client.get(
            url,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lists_detail_fails_for_others_private_list_with_auth_api(self):
        """
        Ensure that `ListDetailView`:

        - return `HTTP_403_FORBIDDEN` when trying to access other's private list, with auth.
        """
        others_private_list = List.objects.filter(
            user_id=1,
            is_public=False,
        ).first()

        url = f"/api/v1/lists/{others_private_list.pk}/"
        response = self.client.get(
            url,
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lists_detail_fails_for_own_private_list_without_auth_api(self):
        """
        Ensure that `ListDetailView`:

        - return `HTTP_403_FORBIDDEN` when trying to access other's private list, without auth.
        """
        others_private_list = List.objects.filter(
            user_id=1,
            is_public=False,
        ).first()

        url = f"/api/v1/lists/{others_private_list.pk}/"
        response = self.client.get(
            url,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag_test("noci")
    def test_lists_detail_for_own_private_list_with_auth_api(self):
        """
        Ensure that `ListDetailView`:

        - return `HTTP_200_OK` when trying to access own private list, with auth;
        - return detailed data for the list, properly serialized.
        """
        own_private_list = List.objects.filter(
            user=self.new_user,
            is_public=False,
        ).first()

        url = f"/api/v1/lists/{own_private_list.pk}/"
        response = self.client.get(
            url,
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        list_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_detail_serialized_data(list_data, own_private_list)

    def test_lists_delete_fails_without_auth_api(self):
        """
        Ensure that `ListDetailView`:

        - return `HTTP_403_FORBIDDEN` when trying to delete a list, without auth.
        """
        for list_instance in List.objects.all():
            url = f"/api/v1/lists/{list_instance.pk}/"
            response = self.client.delete(
                url,
            )

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lists_delete_own_list_with_auth_api(self):
        """
        Ensure that `ListDetailView`:

        - return `HTTP_204_NO_CONTENT` when trying to delete own list, with auth;
        - list is actually deleted.
        """
        own_list = List.objects.create(
            user=self.new_user,
            title="New test list",
        )
        own_list_pk = own_list.pk

        url = f"/api/v1/lists/{own_list.pk}/"
        response = self.client.delete(
            url,
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(List.objects.filter(pk=own_list_pk).count(), 0)

    def test_lists_delete_others_list_fails_with_auth_api(self):
        """
        Ensure that `ListDetailView`:

        - return `HTTP_403_FORBIDDEN` when trying to delete other user's list, with auth.
        """
        for others_list in List.objects.exclude(user=self.new_user):
            url = f"/api/v1/lists/{others_list.pk}/"
            response = self.client.delete(
                url,
                **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
            )

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
