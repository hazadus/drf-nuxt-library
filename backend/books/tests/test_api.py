import json

from django.db.models import Q
from rest_framework.test import APITestCase

from books.models import Book, Author, Publisher, Tag
from users.models import CustomUser


class BooksAPITest(APITestCase):
    """
    Test `books` app DRF API.
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

    def test_book_list_api(self):
        """
        Ensure that `BookListView`:
        - is located at expected URL;
        - return paginated result with expected number of books in one page;
        - return serialized `Book` data as expected from `BookListSerializer`;
        - properly works with `?page=` GET parameter.
        """
        url = "/api/v1/books/"
        response = self.client.get(
            url,
        )

        all_books = Book.objects.all()

        list_page = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(list_page["results"]), 10)
        self.assertEqual(list_page["page"], 1)
        self.assertEqual(list_page["count"], all_books.count())

        # Check every page, every book...
        for current_page in range(1, list_page["total_pages"] + 1):
            url = f"/api/v1/books/?page={current_page}"
            response = self.client.get(
                url,
            )
            self.assertEqual(response.status_code, 200)
            list_page = json.loads(response.content)

            for book in list_page["results"]:
                book_instance = Book.objects.get(pk=book["id"])

                #
                # Ensure `BookListSerializer` return all the data we expect, and the data is correct
                #
                self.assertEqual(book["id"], book_instance.id)
                self.assertEqual(book["title"], book_instance.title)
                self.assertEqual(book["year"], book_instance.year)
                self.assertEqual(book["pages"], book_instance.pages)

                if book_instance.cover_image:
                    self.assertEqual(book["cover_image"], book_instance.cover_image.url)
                    self.assertEqual(
                        book["cover_thumbnail_small"],
                        book_instance.cover_thumbnail_small.url,
                    )
                    self.assertEqual(
                        book["cover_thumbnail_medium"],
                        book_instance.cover_thumbnail_medium.url,
                    )
                    self.assertEqual(
                        book["cover_thumbnail_large"],
                        book_instance.cover_thumbnail_large.url,
                    )

                if book_instance.file:
                    self.assertEqual(book["file"], book_instance.file.url)

                self.assertEqual(
                    book["created"], book_instance.created.astimezone().isoformat()
                )
                self.assertEqual(
                    book["updated"], book_instance.updated.astimezone().isoformat()
                )

                # `user`:
                self.assertEqual(book["user"]["id"], book_instance.user.pk)
                self.assertEqual(book["user"]["username"], book_instance.user.username)
                self.assertEqual(
                    book["user"]["profile_image"], book_instance.user.profile_image.url
                )
                self.assertEqual(
                    book["user"]["profile_image_thumbnail_small"],
                    book_instance.user.profile_image_thumbnail_small.url,
                )
                self.assertEqual(
                    book["user"]["profile_image_thumbnail_large"],
                    book_instance.user.profile_image_thumbnail_large.url,
                )

                # `authors`:
                for author in book["authors"]:
                    author_instance = Author.objects.get(pk=author["id"])
                    self.assertEqual(author["id"], author_instance.pk)
                    self.assertEqual(author["first_name"], author_instance.first_name)
                    self.assertEqual(author["middle_name"], author_instance.middle_name)
                    self.assertEqual(author["last_name"], author_instance.last_name)

                # `publisher`:
                if book["publisher"]:
                    publisher_instance = Publisher.objects.get(
                        pk=book["publisher"]["id"]
                    )
                    self.assertEqual(book["publisher"]["id"], publisher_instance.pk)
                    self.assertEqual(
                        book["publisher"]["title"], publisher_instance.title
                    )

                # `tags`:
                for tag in book["tags"]:
                    tag_instance = Tag.objects.get(pk=tag["id"])
                    self.assertEqual(tag["id"], tag_instance.pk)
                    self.assertEqual(tag["title"], tag_instance.title)
                    if tag_instance.user:
                        self.assertEqual(tag["user"], tag_instance.user.pk)

    def test_book_list_with_query_api(self):
        """
        Check that `BookListView` endpoint with `?query=` parameter return exact same result as we get from DB.
        """
        queries = ["rust", "python", "волк", "мартин", "clean"]

        for query in queries:
            url = f"/api/v1/books/?query={query}"
            response = self.client.get(
                url,
            )

            self.assertEqual(response.status_code, 200)
            list_page = json.loads(response.content)

            queryset = (
                Book.objects.all()
                .filter(
                    Q(title__icontains=query)
                    | Q(authors__last_name__icontains=query)
                    | Q(contents__icontains=query)
                    | Q(description__icontains=query)
                )
                .distinct()
            )

            self.assertEqual(list_page["count"], queryset.count())

            for current_page in range(1, list_page["total_pages"] + 1):
                url = f"/api/v1/books/?query={query}&page={current_page}"
                response = self.client.get(
                    url,
                )

                self.assertEqual(response.status_code, 200)
                list_page = json.loads(response.content)

                for book in list_page["results"]:
                    book_instance = Book.objects.get(pk=book["id"])
                    self.assertTrue(book_instance in queryset.all())
