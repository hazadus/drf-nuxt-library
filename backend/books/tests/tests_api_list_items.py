#
# Tests for `list_items/` endpoint.
# Tests tagged "noci" are excluded when running tests in GutHub Actions (because of missing media files).
#
import json

from rest_framework import status

from books.models import List, Book, ListItem

from .base_api_test_case import BaseAPITest


class ListItemsAPITest(BaseAPITest):
    """
    Test `list_items/` DRF API endpoint.
    """

    def test_list_items_create_with_auth_api(self):
        """
        Ensure that `ListItemCreateView`:

        - correctly creates new `ListItem` in auth'd user's List when correct data posted;
        - returns `HTTP_201_CREATED` and expected serialized data.
        """
        book_instance = Book.objects.first()
        list_instance = List.objects.create(
            user=self.new_user,
            title="New Test List",
            description="Description of the New Test List",
            is_public=True,
        )

        url = "/api/v1/list_items/create/"
        response = self.client.post(
            url,
            {
                "book": book_instance.pk,
                "list": list_instance.pk,
                "description": "Test ListItem",
            },
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        list_item_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(list_item_data["list"], list_instance.pk)
        self.assertEqual(list_item_data["book"], book_instance.pk)
        self.assertEqual(list_item_data["order"], 0)
        self.assertEqual(list_item_data["description"], "Test ListItem")

    def test_list_items_create_fails_with_other_users_list_api(self):
        """
        Ensure that `ListItemCreateView`:

        - fails to create new `ListItem` in other user's List;
        - return `HTTP_403_FORBIDDEN`.
        """
        book_instance = Book.objects.first()
        list_instance = List.objects.filter(user_id__exact=1).first()

        url = "/api/v1/list_items/create/"
        response = self.client.post(
            url,
            {
                "book": book_instance.pk,
                "list": list_instance.pk,  # Other user's list
                "description": "Test ListItem",
            },
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_items_create_fails_adding_book_twice_api(self):
        """
        Ensure that `ListItemCreateView`:

        - fails when trying to add book already present in the list;
        - return `HTTP_400_BAD_REQUEST`
        """
        book_instance = Book.objects.first()
        list_instance = List.objects.create(
            user=self.new_user,
            title="New Test List",
            description="Description of the New Test List",
            is_public=True,
        )
        ListItem.objects.create(
            list=list_instance,
            book=book_instance,
        )

        # Try to add the same book to the same list again...
        url = "/api/v1/list_items/create/"
        response = self.client.post(
            url,
            {
                "book": book_instance.pk,
                "list": list_instance.pk,
                "description": "Test ListItem",
            },
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        list_item_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_items_detail_delete_with_auth_api(self):
        """
        Ensure that `ListItemDetailView`:

        - return `HTTP_204_NO_CONTENT` when trying to DELETE ListItem from auth'd user's list;
        - the ListItem actually gets deleted from database.
        """
        book_instance = Book.objects.first()
        list_instance = List.objects.create(
            user=self.new_user,
            title="New Test List",
            description="Description of the New Test List",
            is_public=True,
        )
        list_item_instance = ListItem.objects.create(
            list=list_instance,
            book=book_instance,
        )
        list_item_pk = list_item_instance.pk
        url = f"/api/v1/list_items/{list_item_pk}/"

        response = self.client.delete(
            url,
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ListItem.objects.filter(pk=list_item_pk).count(), 0)

    def test_list_items_detail_delete_fails_for_other_users_list_with_auth_api(self):
        """
        Ensure that `ListItemDetailView` with auth:

        - return `HTTP_403_FORBIDDEN` when trying to DELETE ListItem from other than auth'd user's list.
        """

        # Get random ListItem - it will be from other user's list:
        list_item_instance = ListItem.objects.first()
        url = f"/api/v1/list_items/{list_item_instance.pk}/"

        response = self.client.delete(
            url,
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_items_detail_delete_fails_withot_auth_api(self):
        """
        Ensure that `ListItemDetailView` without auth:

        - return `HTTP_401_UNAUTHORIZED` when trying to DELETE ListItem from list.
        """

        list_item_instance = ListItem.objects.first()
        url = f"/api/v1/list_items/{list_item_instance.pk}/"

        response = self.client.delete(
            url,
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
