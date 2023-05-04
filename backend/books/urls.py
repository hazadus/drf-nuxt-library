from django.urls import path

from .views import BookListView, BookDetailView, PublisherListView, PublisherDetailView

urlpatterns = [
    path("books/", BookListView.as_view()),
    path("books/<int:book_pk>/", BookDetailView.as_view()),
    path("publishers/", PublisherListView.as_view()),
    path("publishers/<int:pk>/", PublisherDetailView.as_view()),
]
