from django.urls import path

from .views import BookListView, BookDetailView

urlpatterns = [
    path("books/", BookListView.as_view()),
    path("books/<int:book_pk>/", BookDetailView.as_view()),
]
