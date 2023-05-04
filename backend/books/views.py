from django.db.models import QuerySet, Q
from django.http import Http404
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import BookListSerializer, BookDetailSerializer
from .models import Book


class StandardResultsSetPagination(PageNumberPagination):
    """
    Basic pagination class for Book list.
    """

    page_size = 10

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "page": self.page.number,
                "total_pages": self.page.paginator.num_pages,
                "results": data,
            }
        )


class BookListView(ListAPIView):
    """
    List all available books.
    """

    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self) -> QuerySet:
        """
        Filter QuerySet using passed GET parameter `query`.
        """
        queryset = Book.objects.all().filter()
        query = self.request.query_params.get("query", "")

        # NB: strange behavior (item duplication in the list) when filtering by
        # `| Q(authors__last_name__icontains=query)`
        if query:
            queryset = queryset.filter(Q(title__icontains=query))

        return queryset


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
