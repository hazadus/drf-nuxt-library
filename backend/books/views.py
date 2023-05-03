from django.http import Http404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import BookListSerializer, BookDetailSerializer
from .models import Book


class BookListView(APIView):
    """
    List all available books.
    """

    @staticmethod
    def get(request: Request) -> Response:
        """
        Return all available books.
        """
        books = Book.objects.all()
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)


class BookDetailView(APIView):
    """
    Return detailed Book info.
    """

    @staticmethod
    def get_object(book_pk: int) -> Book:
        """
        Return Book instance.
        """
        book = Book.objects.filter(
            pk=book_pk,
        )

        if book:
            return book.first()

        raise Http404

    def get(self, request: Request, book_pk: int) -> Response:
        """
        Return detailed Book info by it's id.
        """
        book = self.get_object(
            book_pk=book_pk,
        )
        serializer = BookDetailSerializer(book)
        return Response(serializer.data)
