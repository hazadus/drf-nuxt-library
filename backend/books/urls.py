from django.urls import path

from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    PublisherListView,
    PublisherDetailView,
    AuthorListView,
    AuthorDetailView,
    AuthorCreateView,
    NoteListView,
)

urlpatterns = [
    path("books/", BookListView.as_view()),
    path("books/<int:pk>/", BookDetailView.as_view()),
    path("books/create/", BookCreateView.as_view()),
    path("authors/", AuthorListView.as_view()),
    path("authors/<int:pk>/", AuthorDetailView.as_view()),
    path("authors/create/", AuthorCreateView.as_view()),
    path("publishers/", PublisherListView.as_view()),
    path("publishers/<int:pk>/", PublisherDetailView.as_view()),
    path("notes/", NoteListView.as_view()),
]
