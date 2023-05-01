from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import BookListSerializer
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
