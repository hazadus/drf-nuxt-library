"""
Module contains serializers for models from `bookmarks` app.

Note about serializer naming:
SomeDetailSerializer - maximum details, with all nested objects serialized.
SomeListSerializer or SomeMinimalSerializer - concise serializer.

For simple models, only "detail" serializers are present.
"""
from rest_framework import serializers

from .models import Tag, Publisher, Author, Book, Note, List, ListItem
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


class AuthorURLRepresentationMixin(serializers.ModelSerializer):
    """
    Deliver consistent relative URLs of author portrait images.
    """

    def to_representation(self, instance):
        """
        Deliver consistent relative URLs of author portrait images.
        Issue: https://forum.djangoproject.com/t/drf-imagefield-serializes-entire-url-with-domain-name/6975
        """
        ret = super().to_representation(instance)
        ret["portrait"] = instance.portrait.url if instance.portrait else ""
        ret["portrait_thumbnail"] = (
            instance.portrait_thumbnail.url if instance.portrait else ""
        )
        return ret


class AuthorDetailSerializer(AuthorURLRepresentationMixin, serializers.ModelSerializer):
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
            "portrait_thumbnail",
        ]


class AuthorCreateSerializer(AuthorURLRepresentationMixin, serializers.ModelSerializer):
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
            "portrait_thumbnail",
        ]


class BookURLRepresentationMixin(serializers.ModelSerializer):
    """
    Deliver consistent relative URLs of cover images and attached file.
    """

    def to_representation(self, instance):
        """
        Deliver consistent relative URLs of cover images and attached file.
        Issue: https://forum.djangoproject.com/t/drf-imagefield-serializes-entire-url-with-domain-name/6975
        """
        ret = super().to_representation(instance)
        ret["cover_image"] = instance.cover_image.url if instance.cover_image else ""
        ret["cover_thumbnail_small"] = (
            instance.cover_thumbnail_small.url if instance.cover_image else ""
        )
        ret["cover_thumbnail_medium"] = (
            instance.cover_thumbnail_medium.url if instance.cover_image else ""
        )
        ret["cover_thumbnail_large"] = (
            instance.cover_thumbnail_large.url if instance.cover_image else ""
        )
        ret["file"] = instance.file.url if instance.file else ""
        return ret


class BookListSerializer(BookURLRepresentationMixin, serializers.ModelSerializer):
    """
    Serializer for Book model - for use in list view.

    NB: "isbn", "description", "contents" are excluded to make serialized data more compact.
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
            "tags",
            "cover_image",
            "cover_thumbnail_small",
            "cover_thumbnail_medium",
            "cover_thumbnail_large",
            "file",
            "created",
            "updated",
        ]


class BookDetailSerializer(BookURLRepresentationMixin, serializers.ModelSerializer):
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
            "cover_thumbnail_small",
            "cover_thumbnail_medium",
            "cover_thumbnail_large",
            "file",
            "created",
            "updated",
        ]


class BookCreateSerializer(BookURLRepresentationMixin, serializers.ModelSerializer):
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
            "cover_thumbnail_small",
            "cover_thumbnail_medium",
            "cover_thumbnail_large",
            "file",
            "created",
            "updated",
        ]


class ListItemDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for `ListItem`.
    """

    book = BookDetailSerializer(many=False)

    class Meta:
        model = ListItem
        fields = [
            "id",
            "order",
            "book",
            "description",
            "created",
            "updated",
        ]


class ListItemListSerializer(serializers.ModelSerializer):
    """
    Compact serializer for `ListItem`.
    """

    book = BookListSerializer(many=False)

    class Meta:
        model = ListItem
        fields = [
            "id",
            "order",
            "book",
            "description",
            "created",
            "updated",
        ]


class ListListSerializer(serializers.ModelSerializer):
    """
    List serializer for user-created `List` of books.
    Much more compact (in terms of data transferred) version than `ListDetailSerializer`.
    """

    user = CustomUserMinimalSerializer(many=False)
    items = ListItemListSerializer(many=True)

    class Meta:
        model = List
        fields = [
            "id",
            "user",
            "title",
            "description",
            "is_public",
            "items",
            "created",
            "updated",
        ]


class ListDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for user-created `List` of books.
    """

    user = CustomUserMinimalSerializer(many=False)
    items = ListItemDetailSerializer(many=True)

    class Meta:
        model = List
        fields = [
            "id",
            "user",
            "title",
            "description",
            "is_public",
            "items",
            "created",
            "updated",
        ]
