from django.test import TestCase

from books.models import Tag, Publisher, Author, Book, List, ListItem, Note
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
    list_title = "Test List"
    note_text = "Note test text"
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
        {
            "authors": None,
            "title": "Book 2 title",
            "year": 2022,
            "pages": 456,
            "publisher": None,
            "isbn": "2345678900123",
            "description": "Book 2 description",
            "contents": "Book 2 contents",
            "tags": None,
        },
        {
            "authors": None,
            "title": "Book 3 title",
            "year": 2021,
            "pages": 789,
            "publisher": None,
            "isbn": "3456789000123",
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
        book_instances = []

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
            book_instances.append(instance)

            instance.authors.add(author_instances[0])
            cls.books[i]["authors"] = author_instances[0]
            instance.tags.add(tag)
            cls.books[i]["tags"] = tag

        # Put all the books into test list
        list_instance = List.objects.create(
            user=cls.user,
            title=cls.list_title,
        )
        for book in book_instances:
            ListItem.objects.create(
                list=list_instance,
                book=book,
            )

        Note.objects.create(
            user=cls.user,
            book=book_instances[0],
            text=cls.note_text,
        )

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
        Ensure that Book model works as expected.
        """
        for book in self.books:
            book_instance = Book.objects.get(isbn=book["isbn"])
            self.assertEqual(str(book_instance), book["title"])
            self.assertEqual(book_instance.user, self.user)
            self.assertEqual(book_instance.title, book["title"])
            self.assertEqual(book_instance.year, book["year"])
            self.assertEqual(book_instance.pages, book["pages"])
            self.assertEqual(book_instance.isbn, book["isbn"])
            self.assertEqual(book_instance.description, book["description"])
            self.assertEqual(book_instance.contents, book["contents"])

    def test_list_model(self):
        """
        Ensure that:
        - List instance is properly created for specified user, `__str__` works as expected, list is private by default.
        """
        list_instance = List.objects.first()
        self.assertEqual(list_instance.user, self.user)
        self.assertEqual(list_instance.title, self.list_title)
        self.assertEqual(str(list_instance), self.list_title)
        self.assertEqual(list_instance.is_public, False)

    def test_listitem_model(self):
        """
        Ensure that ListItem instances:
        - are properly created and ordered (starting from 0);
        - `__str__` works as expected.
        """
        list_instance = List.objects.first()

        for i, list_item in enumerate(list_instance.items.all()):
            self.assertEqual(list_item.order, i)
            self.assertEqual(
                str(list_item),
                "#{order} в {list_title} - {book_title}".format(
                    order=i,
                    list_title=self.list_title,
                    book_title=list_item.book.title,
                ),
            )

    def test_note_model(self):
        """
        Ensure that Note instance:
        - is properly created for specified user;
        - `__str__` works as expected.
        """
        note_instance = Note.objects.first()
        self.assertEqual(note_instance.user, self.user)
        self.assertEqual(note_instance.text, self.note_text)
        self.assertEqual(str(note_instance), self.note_text[:64])
