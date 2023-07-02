from django.db.models import QuerySet, Q
from rest_framework import authentication, permissions, status
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
    CreateAPIView,
    GenericAPIView,
)
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
)
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
    ListListSerializer,
    ListDetailSerializer,
)
from .models import Author, Book, Publisher, Note, List


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
        Create new Book / Author / Publisher / Note, setting `user` field to authenticated user.
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

    serializer_class = BookListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self) -> QuerySet:
        """
        Filter QuerySet using passed GET parameter `query`.
        """
        queryset = (
            Book.objects.all()
            .prefetch_related(
                "authors",
                "tags",
            )
            .select_related(
                "publisher",
                "user",
            )
        )
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

    queryset = (
        Book.objects.all()
        .prefetch_related(
            "authors",
            "tags",
        )
        .select_related(
            "user",
            "publisher",
        )
    )
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

    serializer_class = AuthorDetailSerializer

    def get_queryset(self) -> QuerySet:
        """
        Filter QuerySet by `last_name` using passed GET parameter `query`.
        """
        queryset = Author.objects.all().prefetch_related("user")
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
    Retrieve / partial update / delete Note view.
    Only allow to retrieve, update and delete notes created by authenticated user.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = Note.objects.all()
    serializer_class = NoteDetailSerializer

    def get(self, request, *args, **kwargs):
        """
        Only allow to retrieve notes created by authenticated user.
        """
        instance: Note = self.get_object()
        if instance.user == request.user:
            return self.retrieve(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, *args, **kwargs):
        """
        Partial update.
        Only allow to update notes created by authenticated user.
        """
        instance: Note = self.get_object()
        if instance.user == request.user:
            return self.partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        """
        Only allow to delete notes created by authenticated user.
        """
        instance: Note = self.get_object()
        if instance.user == request.user:
            return self.destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)


class ListListView(ListAPIView):
    """
    List all available book Lists - public or created by authenticated user (not paginated).
    """

    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = ListListSerializer

    def get_queryset(self) -> QuerySet:
        """
        Filter QuerySet - only public lists or lists created by authenticated user.
        Use `?book_id` GET parameter to filter lists only with the book.
        """
        queryset = (
            List.objects.all()
            .prefetch_related(
                "items__book__publisher",
                "items__book__user",
                "items__book__authors",
                "items__book__tags",
            )
            .select_related("user")
        )

        if self.request.auth:
            queryset = queryset.filter(
                Q(is_public=True) | Q(user_id=self.request.user.id)
            )
        else:
            queryset = queryset.filter(is_public=True)

        book_id = self.request.query_params.get("book_id", "")

        if book_id:
            queryset = queryset.filter(
                items__book_id__in=[
                    book_id,
                ]
            )

        return queryset


class ListDetailView(RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    """
    Detailed `List` view / delete view.
    """

    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = ListDetailSerializer

    def get_queryset(self) -> QuerySet:
        """
        Prefetch related fields to reduce number of SQL queries.
        """
        queryset = (
            List.objects.all()
            .prefetch_related(
                "items__book__publisher",
                "items__book__user",
                "items__book__authors",
                "items__book__tags",
            )
            .select_related("user")
        )
        return queryset

    def get(self, request, *args, **kwargs):
        """
        Only allow to retrieve public Lists, or created by authenticated user.
        """
        instance: List = self.get_object()
        if instance.is_public or instance.user == request.user:
            return self.retrieve(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        """
        Only allow author to delete List.
        """
        instance: List = self.get_object()
        if instance.user == request.user:
            return self.destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)
