from django.db.models import QuerySet, Q
from django.http import Http404
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
    CreateAPIView,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    BookListSerializer,
    BookDetailSerializer,
    BookCreateSerializer,
    PublisherDetailSerializer,
    AuthorDetailSerializer,
    AuthorCreateSerializer,
)
from .models import Author, Book, Publisher


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
    List all available books with pagination.
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


class BookCreateView(CreateAPIView):
    """
    Create new book.
    """

    queryset = Book.objects.all()
    serializer_class = BookCreateSerializer


class PublisherListView(ListCreateAPIView):
    """
    List all available publishers (not paginated).
    Create new publisher.
    """

    queryset = Publisher.objects.all()
    serializer_class = PublisherDetailSerializer

    def get_queryset(self) -> QuerySet:
        """
        Filter QuerySet by `title` using passed GET parameter `query`.
        """
        queryset = Publisher.objects.all()
        query = self.request.query_params.get("query", "")

        if query:
            queryset = queryset.filter(title__icontains=query)

        return queryset


class PublisherDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve / update / delete publisher detail view.
    """

    queryset = Publisher.objects.all()
    serializer_class = PublisherDetailSerializer


class AuthorListView(ListAPIView):
    """
    List all available authors (not paginated).
    """

    queryset = Author.objects.all()
    serializer_class = AuthorDetailSerializer

    def get_queryset(self) -> QuerySet:
        """
        Filter QuerySet by `last_name` using passed GET parameter `query`.
        """
        queryset = Author.objects.all()
        query = self.request.query_params.get("query", "")

        if query:
            queryset = queryset.filter(last_name__icontains=query)

        return queryset


class AuthorCreateView(CreateAPIView):
    """
    Create new author.
    """

    queryset = Author.objects.all()
    serializer_class = AuthorCreateSerializer


class AuthorDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve / update / delete author detail view.
    """

    queryset = Author.objects.all()
    serializer_class = AuthorDetailSerializer
