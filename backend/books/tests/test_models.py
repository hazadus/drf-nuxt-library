from django.test import TestCase

from books.models import Tag, Publisher, Author, Book
from users.models import CustomUser


class BooksAppModelsTest(TestCase):
    """
    Test models from `books` app.
    """

    username = "testuser"
    password = "password"
    tag_title = "TestTag"
    publisher_title = "Test Press, Inc."
    user = None
    authors = [
        {
            "first_name": "Ivan",
            "middle_name": "Ivanovich",
            "last_name": "Ivanov",
            "expected_full_name": "Ivanov Ivan Ivanovich",
            "description": "Description - Ivanov I.I.",
        },
        {
            "first_name": "Petr",
            "middle_name": "",
            "last_name": "Petrov",
            "expected_full_name": "Petrov Petr",
            "description": "Description - Petrov P.",
        },
        {
            "first_name": "",
            "middle_name": "",
            "last_name": "Sidorov",
            "expected_full_name": "Sidorov",
            "description": "Description - Sidorov",
        },
    ]
    books = [
        {
            "authors": None,
            "title": "Book 1 title",
            "year": 2023,
            "pages": 123,
            "publisher": None,
            "isbn": "1234567890123",
            "description": "Book 1 description",
            "contents": "Book 1 contents",
            "tags": None,
        },
    ]

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(cls.username, password=cls.password)
        tag = Tag.objects.create(user=cls.user, title=cls.tag_title)
        publisher = Publisher.objects.create(user=cls.user, title=cls.publisher_title)
        author_instances = []

        for author in cls.authors:
            author_instances.append(
                Author.objects.create(
                    user=cls.user,
                    first_name=author["first_name"],
                    middle_name=author["middle_name"],
                    last_name=author["last_name"],
                    description=author["description"],
                )
            )

        for i, book in enumerate(cls.books):
            instance = Book.objects.create(
                user=cls.user,
                title=book["title"],
                year=book["year"],
                pages=book["pages"],
                publisher=publisher,
                isbn=book["isbn"],
                description=book["description"],
                contents=book["contents"],
            )
            instance.authors.add(author_instances[0])
            cls.books[i]["authors"] = author_instances[0]
            instance.tags.add(tag)
            cls.books[i]["tags"] = tag

    def test_tag_and_publisher_models(self):
        """
        Ensure that Tag, Publisher are created and correctly represented when converted to string.
        """
        self.assertEqual(str(Tag.objects.first()), self.tag_title)
        self.assertEqual(str(Publisher.objects.first()), self.publisher_title)

    def test_author_model(self):
        """
        Ensure that Authors are correctly created and `__str__` and `full_name` work as expected.
        """
        for author in self.authors:
            author_instance = Author.objects.get(last_name=author["last_name"])
            self.assertEqual(author_instance.user, self.user)
            self.assertEqual(author_instance.last_name, author["last_name"])
            self.assertEqual(author_instance.first_name, author["first_name"])
            self.assertEqual(author_instance.middle_name, author["middle_name"])
            self.assertEqual(author_instance.description, author["description"])
            self.assertEqual(author_instance.full_name, author["expected_full_name"])
            self.assertEqual(str(author_instance), author["expected_full_name"])

    def test_books_model(self):
        """
        Ensure that Book model works as expecteed.
        """
        for book in self.books:
            book_instance = Book.objects.get(isbn=book["isbn"])
            self.assertEqual(str(book_instance), book["title"])
            self.assertEqual(book_instance.title, book["title"])
            self.assertEqual(book_instance.year, book["year"])
            self.assertEqual(book_instance.pages, book["pages"])
            self.assertEqual(book_instance.isbn, book["isbn"])
            self.assertEqual(book_instance.description, book["description"])
            self.assertEqual(book_instance.contents, book["contents"])
