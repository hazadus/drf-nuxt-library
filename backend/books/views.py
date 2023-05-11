from django.db.models import QuerySet, Q
from rest_framework import authentication, permissions, status
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
    CreateAPIView,
)
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .serializers import (
    BookListSerializer,
    BookDetailSerializer,
    BookCreateSerializer,
    PublisherDetailSerializer,
    AuthorDetailSerializer,
    AuthorCreateSerializer,
    NoteDetailSerializer,
)
from .models import Author, Book, Publisher, Note


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


class CreateAsAuthenticatedUser(CreateModelMixin):
    """
    Mixin to set `user` field to authenticated user for Book / Author / Publisher / Tag
    """

    def create(self, request, *args, **kwargs):
        """
        Create new Book / Author / Publisher / Tag, setting `user` field to authenticated user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
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

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(authors__last_name__icontains=query)
                | Q(contents__icontains=query)
                | Q(description__icontains=query)
            ).distinct()

        return queryset


class BookDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve / update / delete Book detail view.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer


class BookCreateView(CreateAsAuthenticatedUser, CreateAPIView):
    """
    Create new book.
    Set `user` field to authenticated user.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = Book.objects.all()
    serializer_class = BookCreateSerializer


class PublisherListView(CreateAsAuthenticatedUser, ListCreateAPIView):
    """
    List all available publishers (not paginated).
    Create new publisher. Set `user` field to authenticated user.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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


class AuthorCreateView(CreateAsAuthenticatedUser, CreateAPIView):
    """
    Create new author.
    Set `user` field to authenticated user.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = Author.objects.all()
    serializer_class = AuthorCreateSerializer


class AuthorDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve / update / delete author detail view.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Author.objects.all()
    serializer_class = AuthorDetailSerializer


class NoteListView(ListAPIView):
    """
    List all available Notes created by authorized user (not paginated).
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = Note.objects.all()
    serializer_class = NoteDetailSerializer

    def get_queryset(self) -> QuerySet:
        """
        Filter QuerySet by authenticated user's id and GET parameter `book_id` (if present).
        """
        queryset = Note.objects.all().filter(user_id__exact=self.request.user.id)

        book_id = self.request.query_params.get("book_id", "")

        if book_id:
            queryset = queryset.filter(book_id__exact=book_id)

        return queryset


class NoteCreateView(CreateAsAuthenticatedUser, CreateAPIView):
    """
    Create new Note.
    Set `user` field to authenticated user.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = Note.objects.all()
    serializer_class = NoteDetailSerializer


class NoteDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve / update / delete Note view.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = Note.objects.all()
    serializer_class = NoteDetailSerializer
