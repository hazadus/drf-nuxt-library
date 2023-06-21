import json

from django.conf import settings

from rest_framework.test import APITestCase

from books.models import List, Book, ListItem, Author, Publisher, Tag
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

    def check_user_minimal_serialized_data(
        self, user_data: dict, user_instance: CustomUser
    ):
        """
        Check each field serialized using `CustomUserMinimalSerializer`.
        """

        self.assertEqual(user_data["id"], user_instance.pk)
        self.assertEqual(user_data["username"], user_instance.username)

        if user_instance.profile_image:
            self.assertEqual(
                user_data["profile_image"],
                user_instance.profile_image.url,
            )
            self.assertEqual(
                user_data["profile_image_thumbnail_small"],
                user_instance.profile_image_thumbnail_small.url,
            )
            self.assertEqual(
                user_data["profile_image_thumbnail_large"],
                user_instance.profile_image_thumbnail_large.url,
            )

    def check_book_list_serialized_data(self, book_data: dict, book_instance: Book):
        """
        Ensure `BookListSerializer` return all the data we expect, and the data is correct.
        """
        self.assertEqual(book_data["id"], book_instance.id)
        self.assertEqual(book_data["title"], book_instance.title)
        self.assertEqual(book_data["year"], book_instance.year)
        self.assertEqual(book_data["pages"], book_instance.pages)

        if book_instance.cover_image:
            self.assertEqual(book_data["cover_image"], book_instance.cover_image.url)
            self.assertEqual(
                book_data["cover_thumbnail_small"],
                book_instance.cover_thumbnail_small.url,
            )
            self.assertEqual(
                book_data["cover_thumbnail_medium"],
                book_instance.cover_thumbnail_medium.url,
            )
            self.assertEqual(
                book_data["cover_thumbnail_large"],
                book_instance.cover_thumbnail_large.url,
            )

        if book_instance.file:
            self.assertEqual(book_data["file"], book_instance.file.url)

        self.assertEqual(
            book_data["created"], book_instance.created.astimezone().isoformat()
        )
        self.assertEqual(
            book_data["updated"], book_instance.updated.astimezone().isoformat()
        )

        #  `user` (optional) serialized with `CustomUserMinimalSerializer`
        if book_instance.user:
            self.check_user_minimal_serialized_data(
                user_data=book_data["user"], user_instance=book_instance.user
            )

        # `authors`:
        for author in book_data["authors"]:
            author_instance = Author.objects.get(pk=author["id"])
            self.assertEqual(author["id"], author_instance.pk)
            self.assertEqual(author["first_name"], author_instance.first_name)
            self.assertEqual(author["middle_name"], author_instance.middle_name)
            self.assertEqual(author["last_name"], author_instance.last_name)

        # `publisher`:
        if book_data["publisher"]:
            publisher_instance = Publisher.objects.get(pk=book_data["publisher"]["id"])
            self.assertEqual(book_data["publisher"]["id"], publisher_instance.pk)
            self.assertEqual(book_data["publisher"]["title"], publisher_instance.title)

        # `tags`:
        for tag in book_data["tags"]:
            tag_instance = Tag.objects.get(pk=tag["id"])
            self.assertEqual(tag["id"], tag_instance.pk)
            self.assertEqual(tag["title"], tag_instance.title)
            if tag_instance.user:
                self.assertEqual(tag["user"], tag_instance.user.pk)

    def check_list_item_list_serialized_data(
        self, list_item_data: dict, list_item_instance: ListItem
    ):
        """
        Check each field serialized using `ListItemListSerializer`.
        """
        self.assertEqual(list_item_data["id"], list_item_instance.pk)
        self.assertEqual(list_item_data["order"], list_item_instance.order)
        self.assertEqual(list_item_data["description"], list_item_instance.description)
        self.assertEqual(
            list_item_data["created"],
            list_item_instance.created.astimezone().isoformat(),
        )
        self.assertEqual(
            list_item_data["updated"],
            list_item_instance.updated.astimezone().isoformat(),
        )

        self.check_book_list_serialized_data(
            book_data=list_item_data["book"], book_instance=list_item_instance.book
        )

    def check_list_serialized_data(self, list_data: dict, list_instance: List) -> None:
        """
        Check each field serialized using `ListListSerializer`.
        """
        self.assertEqual(list_data["id"], list_instance.pk)

        # `user` (optional) serialized with `CustomUserMinimalSerializer`
        if list_instance.user:
            self.check_user_minimal_serialized_data(
                user_data=list_data["user"], user_instance=list_instance.user
            )

        self.assertEqual(list_data["title"], list_instance.title)
        self.assertEqual(list_data["description"], list_instance.description)
        self.assertEqual(list_data["is_public"], list_instance.is_public)
        self.assertEqual(
            list_data["created"], list_instance.created.astimezone().isoformat()
        )
        self.assertEqual(
            list_data["updated"], list_instance.updated.astimezone().isoformat()
        )

        # `items` serialized with `ListItemListSerializer`
        for list_item_data in list_data["items"]:
            list_item_instance = ListItem.objects.get(pk=list_item_data["id"])
            self.check_list_item_list_serialized_data(
                list_item_data=list_item_data, list_item_instance=list_item_instance
            )

    def check_book_detail_serialized_data(self, book_data: dict, book_instance: Book):
        """
        Check each field serialized using `BookDetailSerializer`.
        """
        self.assertEqual(book_data["id"], book_instance.pk)
        self.assertEqual(book_data["title"], book_instance.title)
        self.assertEqual(book_data["year"], book_instance.year)
        self.assertEqual(book_data["pages"], book_instance.pages)
        self.assertEqual(book_data["isbn"], book_instance.isbn)
        self.assertEqual(book_data["description"], book_instance.description)
        self.assertEqual(book_data["contents"], book_instance.contents)

        if book_instance.cover_image:
            self.assertEqual(book_data["cover_image"], book_instance.cover_image.url)
            self.assertEqual(
                book_data["cover_thumbnail_small"],
                book_instance.cover_thumbnail_small.url,
            )
            self.assertEqual(
                book_data["cover_thumbnail_medium"],
                book_instance.cover_thumbnail_medium.url,
            )
            self.assertEqual(
                book_data["cover_thumbnail_large"],
                book_instance.cover_thumbnail_large.url,
            )

        if book_instance.file:
            self.assertEqual(book_data["file"], book_instance.file.url)

        self.assertEqual(
            book_data["created"], book_instance.created.astimezone().isoformat()
        )
        self.assertEqual(
            book_data["updated"], book_instance.updated.astimezone().isoformat()
        )

        #  `user` (optional) serialized with `CustomUserMinimalSerializer`
        if book_instance.user:
            self.check_user_minimal_serialized_data(
                user_data=book_data["user"], user_instance=book_instance.user
            )

        # `authors`:
        for author in book_data["authors"]:
            author_instance = Author.objects.get(pk=author["id"])
            self.assertEqual(author["id"], author_instance.pk)
            self.assertEqual(author["first_name"], author_instance.first_name)
            self.assertEqual(author["middle_name"], author_instance.middle_name)
            self.assertEqual(author["last_name"], author_instance.last_name)
            self.assertEqual(author["description"], author_instance.description)

            # `user` of `author` serialized with `CustomUserMinimalSerializer`:
            if author_instance.user:
                self.check_user_minimal_serialized_data(
                    user_data=author["user"], user_instance=author_instance.user
                )

            if author_instance.portrait:
                self.assertEqual(author["portrait"], author_instance.portrait.url)
                self.assertEqual(
                    author["portrait_thumbnail"],
                    author_instance.portrait_thumbnail.url,
                )

        # `publisher`:
        if book_instance.publisher:
            self.assertEqual(book_data["publisher"]["id"], book_instance.publisher.pk)
            self.assertEqual(
                book_data["publisher"]["title"], book_instance.publisher.title
            )

        # `tags`:
        for tag in book_data["tags"]:
            tag_instance = Tag.objects.get(pk=tag["id"])
            self.assertEqual(tag["id"], tag_instance.pk)
            self.assertEqual(tag["title"], tag_instance.title)
            if tag_instance.user:
                self.assertEqual(tag["user"], tag_instance.user.pk)

    def check_list_item_detail_serialized_data(
        self, list_item_data: dict, list_item_instance: ListItem
    ):
        """
        Check each field serialized using `ListItemDetailSerializer`.
        """
        self.assertEqual(list_item_data["id"], list_item_instance.pk)
        self.assertEqual(list_item_data["order"], list_item_instance.order)
        self.assertEqual(list_item_data["description"], list_item_instance.description)
        self.assertEqual(
            list_item_data["created"],
            list_item_instance.created.astimezone().isoformat(),
        )
        self.assertEqual(
            list_item_data["updated"],
            list_item_instance.updated.astimezone().isoformat(),
        )

        # `book` serialized with `BookDetailSerializer`
        self.check_book_detail_serialized_data(
            book_data=list_item_data["book"], book_instance=list_item_instance.book
        )

    def check_detail_serialized_data(
        self, list_data: dict, list_instance: List
    ) -> None:
        """
        Check each field serialized using `ListDetailSerializer`.
        """
        self.assertEqual(list_data["id"], list_instance.pk)

        # `user` (optional) serialized with `CustomUserMinimalSerializer`
        if list_instance.user:
            self.check_user_minimal_serialized_data(
                user_data=list_data["user"], user_instance=list_instance.user
            )

        self.assertEqual(list_data["title"], list_instance.title)
        self.assertEqual(list_data["description"], list_instance.description)
        self.assertEqual(list_data["is_public"], list_instance.is_public)
        self.assertEqual(
            list_data["created"], list_instance.created.astimezone().isoformat()
        )
        self.assertEqual(
            list_data["updated"], list_instance.updated.astimezone().isoformat()
        )

        # `items` serialized with `ListItemDetailSerializer`
        for list_item_data in list_data["items"]:
            list_item_instance = ListItem.objects.get(pk=list_item_data["id"])
            self.check_list_item_detail_serialized_data(
                list_item_data=list_item_data, list_item_instance=list_item_instance
            )
