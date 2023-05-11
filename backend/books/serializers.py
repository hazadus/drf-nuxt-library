"""
Module contains serializers for models from `bookmarks` app.

Note about serializer naming:
SomeDetailSerializer - maximum details, with all nested objects serialized.
SomeListSerializer or SomeMinimalSerializer - concise serializer

For simple models, only "detail" serializers are created.
"""
from rest_framework import serializers

from .models import Tag, Publisher, Author, Book, Note
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


class NoteDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Note model - detailed.
    """

    class Meta:
        model = Note
        fields = [
            "id",
            "user",
            "book",
            "text",
            "created",
            "updated",
        ]


class AuthorMinimalSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model - used for Book list.
    """

    class Meta:
        model = Author
        fields = [
            "id",
            "first_name",
            "middle_name",
            "last_name",
        ]


class AuthorDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model - detailed.
    """

    user = CustomUserMinimalSerializer(many=False)

    class Meta:
        model = Author
        fields = [
            "id",
            "user",
            "first_name",
            "middle_name",
            "last_name",
            "description",
            "portrait",
        ]

    def to_representation(self, instance):
        """
        Deliver consistent relative URLs of author portrait images.
        Issue: https://forum.djangoproject.com/t/drf-imagefield-serializes-entire-url-with-domain-name/6975
        """
        ret = super().to_representation(instance)
        ret["portrait"] = instance.portrait.url if instance.portrait else ""
        return ret


class AuthorCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model - used to create new authors.
    """

    class Meta:
        model = Author
        fields = [
            "id",
            "user",
            "first_name",
            "middle_name",
            "last_name",
            "description",
            "portrait",
        ]

    def to_representation(self, instance):
        """
        Deliver consistent relative URLs of author portrait images.
        Issue: https://forum.djangoproject.com/t/drf-imagefield-serializes-entire-url-with-domain-name/6975
        """
        ret = super().to_representation(instance)
        ret["portrait"] = instance.portrait.url if instance.portrait else ""
        return ret


class BookListSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model - for use in list view.
    """

    user = CustomUserMinimalSerializer(many=False)
    authors = AuthorMinimalSerializer(many=True)
    publisher = PublisherDetailSerializer(many=False)
    tags = TagDetailSerializer(many=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "user",
            "authors",
            "title",
            "publisher",
            "year",
            "pages",
            "isbn",
            "description",
            "contents",
            "tags",
            "cover_image",
            "file",
            "created",
            "updated",
        ]

    def to_representation(self, instance):
        """
        Deliver consistent relative URLs of cover images and attached file.
        Issue: https://forum.djangoproject.com/t/drf-imagefield-serializes-entire-url-with-domain-name/6975
        """
        ret = super().to_representation(instance)
        ret["cover_image"] = instance.cover_image.url if instance.cover_image else ""
        ret["file"] = instance.file.url if instance.file else ""
        return ret


class BookDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model - for detailed view.
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
            "publisher",
            "year",
            "pages",
            "isbn",
            "description",
            "contents",
            "tags",
            "cover_image",
            "file",
            "created",
            "updated",
        ]

    def to_representation(self, instance):
        """
        Deliver consistent relative URLs of cover images and attached file.
        Issue: https://forum.djangoproject.com/t/drf-imagefield-serializes-entire-url-with-domain-name/6975
        """
        ret = super().to_representation(instance)
        ret["cover_image"] = instance.cover_image.url if instance.cover_image else ""
        ret["file"] = instance.file.url if instance.file else ""
        return ret


class BookCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model - to create new books.
    """

    class Meta:
        model = Book
        fields = [
            "id",
            "user",
            "authors",
            "title",
            "publisher",
            "year",
            "pages",
            "isbn",
            "description",
            "contents",
            "tags",
            "cover_image",
            "file",
            "created",
            "updated",
        ]
