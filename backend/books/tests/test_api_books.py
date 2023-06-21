#
# Tests for `books/` endpoint.
# Tests tagged "noci" are excluded when running tests in GutHub Actions (because of missing media files).
#
import json

from django.db.models import Q
from django.test import tag as tag_test
from rest_framework import status

from books.models import Book, Author, Tag

from .base_api_test_case import BaseAPITest


class BooksAPITest(BaseAPITest):
    """
    Test `books/` DRF API endpoint.
    """

    @tag_test("noci")
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
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

                self.check_book_list_serialized_data(
                    book_data=book, book_instance=book_instance
                )

    @tag_test("noci")
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

            self.assertEqual(response.status_code, status.HTTP_200_OK)
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

    @tag_test("noci")
    def test_book_detail_api(self):
        """
        Ensure that `BookDetailView` endpoint:

        - is located where expected;
        - return full and correct data for every book in DB.
        """
        for book_instance in Book.objects.all():
            url = f"/api/v1/books/{book_instance.pk}/"
            response = self.client.get(
                url,
            )

            book = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.check_book_detail_serialized_data(
                book_data=book, book_instance=book_instance
            )

    def test_book_create_fails_when_unauthorized(self):
        """
        Ensure that `BookCreateView` return `HTTP_401_UNAUTHORIZED` error when trying to POST a book without auth.
        """
        url = "/api/v1/books/create/"
        response = self.client.post(
            url,
            {
                "user": self.new_user.pk,
                "title": "Test Book",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_book_create_with_min_data_api(self):
        """
        Ensure that `BookCreateView`:

        - correctly creates new book with authenticated user set as author (using `CreateAsAuthenticatedUser` mixin);
        - title and one author is enough to create a book instance.
        """
        url = "/api/v1/books/create/"
        book_title = "Test book"
        author_instance = Author.objects.first()
        response = self.client.post(
            url,
            {
                "title": book_title,
                "authors": [
                    author_instance.id,
                ],
            },
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )
        book_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(book_data["user"], self.new_user.pk)
        self.assertEqual(book_data["title"], book_title)
        self.assertEqual(book_data["authors"][0], author_instance.pk)

    def test_book_create_fails_without_author_api(self):
        """
        Ensure that `BookCreateView` fails to create new book for authenticated user, when author isn't specified.
        """
        url = "/api/v1/books/create/"
        book_title = "Test book"
        author_instance = Author.objects.first()
        response = self.client.post(
            url,
            {
                "title": book_title,
                "authors": [],
            },
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )
        book_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
