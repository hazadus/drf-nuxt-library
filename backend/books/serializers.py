from rest_framework import serializers

from .models import Tag, Publisher, Author, Book
from users.serializers import CustomUserMinimalSerializer


class TagDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model - detailed.
    """

    class Meta:
        model = Tag
        fields = [
            "id",
            "title",
            "user",
        ]


class PublisherDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Publisher model - detailed.
    """

    class Meta:
        model = Publisher
        fields = [
            "id",
            "title",
        ]


class AuthorDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model - detailed.
    """

    class Meta:
        model = Author
        fields = [
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "description",
        ]


class BookListSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model - for use in list view.
    """

    user = CustomUserMinimalSerializer(many=False)
    authors = AuthorDetailSerializer(many=True)
    publisher = PublisherDetailSerializer(many=False)
    tags = TagDetailSerializer(many=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "user",
            "authors",
            "title",
            "year",
            "publisher",
            "isbn",
            "description",
            "contents",
            "tags",
            "cover_image",
            "file",
            "created",
            "updated",
        ]


class BookCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model - to create new books.
    """

    class Meta:
        model = Book
        fields = [
            "user",
            "authors",
            "title",
            "year",
            "publisher",
            "contents",
            "tags",
            "cover_image",
            "file",
        ]
