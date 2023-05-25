from django import forms
from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
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


class AuthorAdminForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[
            "portrait"
        ].widget.template_name = "books/widgets/author_portrait.html"


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Configures admin panel views for Author.
    """

    form = AuthorAdminForm
    list_display = [
        "portrait_preview",
        "full_name",
        "has_description",
        "user",
    ]
    list_display_links = [
        "portrait_preview",
        "full_name",
    ]
    fieldsets = [
        (
            _("Имя автора"),
            {
                "fields": [
                    "last_name",
                    "first_name",
                    "middle_name",
                ]
            },
        ),
        (
            _("Информация об авторе"),
            {
                "fields": [
                    "description",
                    "portrait",
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
    ]

    def portrait_preview(self, obj: Author) -> str:
        if obj.portrait:
            return mark_safe(
                render_to_string(
                    "books/widgets/author_portrait_preview.html",
                    {
                        "author": obj,
                    },
                )
            )
        return ""

    portrait_preview.short_description = _("Портрет")

    def has_description(self, obj: Author) -> bool:
        return bool(obj.description)

    has_description.short_description = _("Есть описание")
    has_description.boolean = True


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

    form = BookAdminForm
    list_display = [
        "cover_preview",
        "title",
        "publisher",
        "user",
        "year",
        "created",
    ]
    list_display_links = [
        "cover_preview",
        "title",
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

    def cover_preview(self, obj: Book) -> str:
        if obj.cover_image:
            return mark_safe(
                render_to_string(
                    "books/widgets/book_cover_image_preview.html",
                    {
                        "book": obj,
                    },
                )
            )
        return ""

    cover_preview.short_description = _("Обложка")


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
