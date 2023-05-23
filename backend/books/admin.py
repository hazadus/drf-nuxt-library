from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Tag, Publisher, Author, Book, Note, BookCard, List, ListItem


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Configures admin panel views for Tag.
    """

    model = Tag
    list_display = [
        "title",
        "user",
    ]


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    """
    Configures admin panel views for Publisher.
    """

    model = Publisher
    list_display = [
        "title",
        "user",
    ]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Configures admin panel views for Author.
    """

    model = Author
    list_display = [
        "full_name",
        "user",
    ]


class BookAdminForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[
            "cover_image"
        ].widget.template_name = "books/widgets/book_cover_image.html"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Configures admin panel views for Book.
    """

    # model = Book
    form = BookAdminForm
    list_display = [
        "title",
        "publisher",
        "user",
        "year",
        "created",
    ]
    readonly_fields = [
        "created",
        "updated",
    ]
    fieldsets = [
        (
            _("Основная информация о книге"),
            {
                "fields": [
                    "title",
                    "authors",
                    "description",
                    "contents",
                ]
            },
        ),
        (
            _("Издание"),
            {
                "fields": [
                    "publisher",
                    "year",
                    "pages",
                    "isbn",
                ]
            },
        ),
        (
            _("Метки"),
            {
                "fields": [
                    "tags",
                ]
            },
        ),
        (
            _("Файлы"),
            {
                "fields": [
                    "cover_image",
                    "file",
                ]
            },
        ),
        (
            _("Куратор"),
            {
                "fields": [
                    "user",
                ]
            },
        ),
        (
            _("Время создания и изменения записи"),
            {
                "fields": [
                    "created",
                    "updated",
                ]
            },
        ),
    ]


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """
    Configures admin panel views for Note.
    """

    model = Note
    list_display = [
        "text",
        "book",
        "user",
    ]
    readonly_fields = [
        "created",
        "updated",
    ]


@admin.register(BookCard)
class BookCardAdmin(admin.ModelAdmin):
    """
    Configures admin panel views for BookCard.
    """

    model = BookCard
    list_display = [
        "book",
        "user",
        "is_favorite",
        "want_to_read",
        "is_reading",
        "is_read",
        "created",
    ]
    readonly_fields = [
        "created",
        "updated",
    ]


class ListItemInline(admin.TabularInline):
    model = ListItem
    extra = 0


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    """
    Configures admin views for List.
    """

    model = List
    list_display = [
        "title",
        "user",
        "is_public",
        "created",
    ]
    inlines = [ListItemInline]
    readonly_fields = [
        "created",
        "updated",
    ]


@admin.register(ListItem)
class ListItemAdmin(admin.ModelAdmin):
    """
    Configures admin views for ListItem.
    """

    model = ListItem
    list_display = [
        "position",
        "book",
        "list",
        "created",
    ]
    readonly_fields = [
        "created",
        "updated",
    ]
