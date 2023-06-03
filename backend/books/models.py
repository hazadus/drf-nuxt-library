from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit, SmartResize
from ordered_model.models import OrderedModel


class Tag(models.Model):
    """
    Represents a tag assigned to the book.
    """

    user = models.ForeignKey(
        verbose_name=_("пользователь"),
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="tags_created",
        blank=True,
        null=True,
        default=None,
    )
    title = models.CharField(
        verbose_name=_("название"),
        max_length=32,
    )

    class Meta:
        ordering = ["title"]
        verbose_name = _("метка")
        verbose_name_plural = _("метки")

    def __str__(self):
        return self.title


class Publisher(models.Model):
    """
    Represents book publisher.
    """

    user = models.ForeignKey(
        verbose_name=_("пользователь"),
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="publishers_created",
        blank=True,
        null=True,
        default=None,
    )
    title = models.CharField(
        verbose_name=_("название"),
        max_length=128,
    )

    class Meta:
        ordering = ["title"]
        verbose_name = _("издательство")
        verbose_name_plural = _("издательства")

    def __str__(self):
        return self.title


class Author(models.Model):
    """
    Represents book author.
    """

    user = models.ForeignKey(
        verbose_name=_("пользователь"),
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="authors_created",
        blank=True,
        null=True,
        default=None,
    )
    first_name = models.CharField(
        verbose_name=_("имя"),
        max_length=32,
        blank=True,
        null=True,
    )
    middle_name = models.CharField(
        verbose_name=_("отчетство"),
        max_length=32,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        verbose_name=_("фамилия"),
        max_length=32,
    )
    description = models.TextField(
        verbose_name=_("об авторе"),
        blank=True,
        null=True,
        default=None,
    )
    portrait = models.ImageField(
        verbose_name=_("портрет"),
        null=True,
        blank=True,
        upload_to="images/authors/",
    )
    # NB: from `django-imagekit` docs: ImageSpecFields are virtual — they add no fields to your database and don't
    # require a database.
    portrait_thumbnail = ImageSpecField(
        source="portrait",
        processors=[SmartResize(width=132, height=176, upscale=True)],
        format="JPEG",
        options={"quality": 100},
    )

    class Meta:
        ordering = ["last_name"]
        verbose_name = _("автор")
        verbose_name_plural = _("авторы")

    def __str__(self):
        return self.full_name

    @property
    def full_name(self) -> str:
        """
        Return author's full name.
        """
        full_name = self.last_name
        full_name += " " + str(self.first_name) if self.first_name else ""
        full_name += " " + str(self.middle_name) if self.middle_name else ""
        return str(full_name)


class Book(models.Model):
    """
    Represents a book.
    """

    user = models.ForeignKey(
        verbose_name=_("пользователь"),
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="books_created",
        blank=True,
        null=True,
        default=None,
    )
    authors = models.ManyToManyField(
        verbose_name=_("авторы"),
        to=Author,
        related_name="books",
    )
    title = models.CharField(
        verbose_name=_("название"),
        max_length=512,
    )
    year = models.IntegerField(
        verbose_name=_("год издания"),
        null=True,
        blank=True,
    )
    pages = models.IntegerField(
        verbose_name=_("количество страниц"),
        null=True,
        blank=True,
    )
    publisher = models.ForeignKey(
        verbose_name=_("идательство"),
        to=Publisher,
        on_delete=models.CASCADE,
        related_name="books",
        blank=True,
        null=True,
        default=None,
    )
    isbn = models.CharField(
        verbose_name="ISBN",
        max_length=13,
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name=_("описание"),
        blank=True,
        null=True,
        default=None,
    )
    contents = models.TextField(
        verbose_name=_("содержание"),
        blank=True,
        null=True,
        default=None,
    )
    tags = models.ManyToManyField(
        verbose_name=_("метки"),
        to=Tag,
        related_name="books",
        blank=True,
    )
    cover_image = models.ImageField(
        verbose_name=_("обложка"),
        null=True,
        blank=True,
        upload_to="images/covers/",
    )
    # NB: from `django-imagekit` docs: ImageSpecFields are virtual — they add no fields to your database and don't
    # require a database.
    cover_thumbnail_small = ImageSpecField(
        source="cover_image",
        processors=[ResizeToFit(width=64, upscale=True)],
        format="JPEG",
        options={"quality": 100},
    )
    cover_thumbnail_medium = ImageSpecField(
        source="cover_image",
        processors=[ResizeToFit(width=128, upscale=True)],
        format="JPEG",
        options={"quality": 100},
    )
    cover_thumbnail_large = ImageSpecField(
        source="cover_image",
        processors=[ResizeToFit(width=256, upscale=True)],
        format="JPEG",
        options={"quality": 100},
    )
    file = models.FileField(
        verbose_name=_("файл книги"),
        null=True,
        blank=True,
        upload_to="books/",
    )
    created = models.DateTimeField(verbose_name=_("создана"), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_("изменена"), auto_now=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = _("книга")
        verbose_name_plural = _("книги")

    def __str__(self):
        return "{book}".format(
            book=self.title,
        )


class Note(models.Model):
    """
    Represents user's note for a book.
    """

    user = models.ForeignKey(
        verbose_name=_("пользователь"),
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="notes",
    )
    book = models.ForeignKey(
        verbose_name=_("книга"),
        to=Book,
        on_delete=models.CASCADE,
        related_name="notes",
    )
    text = models.TextField(
        verbose_name=_("заметка"),
    )
    created = models.DateTimeField(verbose_name=_("создана"), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_("изменена"), auto_now=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = _("заметка")
        verbose_name_plural = _("заметки")

    def __str__(self):
        return self.text[:64]


class BookCard(models.Model):
    """
    Represents user's "ownership" of the book, when user adds the book to his virtual library.
    """

    book = models.ForeignKey(
        verbose_name=_("книга"),
        to=Book,
        on_delete=models.CASCADE,
        related_name="book_cards",
    )
    user = models.ForeignKey(
        verbose_name=_("пользователь"),
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="book_cards",
    )
    is_favorite = models.BooleanField(
        verbose_name=_("избранная"),
        default=False,
    )
    want_to_read = models.BooleanField(
        verbose_name=_("хочу прочитать"),
        default=False,
    )
    is_reading = models.BooleanField(
        verbose_name=_("читаю сейчас"),
        default=False,
    )
    is_read = models.BooleanField(
        verbose_name=_("прочитана"),
        default=False,
    )
    read_on = models.DateTimeField(
        verbose_name=_("дата прочтения"),
        blank=True,
        null=True,
    )
    created = models.DateTimeField(verbose_name=_("создана"), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_("изменена"), auto_now=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = _("карточка книги")
        verbose_name_plural = _("карточки книг")

    def __str__(self):
        return "{book} у {user}".format(
            book=self.book,
            user=self.user,
        )


class List(models.Model):
    """
    Represents user-created list containing arbitrary number of books (`ListItem`s).
    """

    user = models.ForeignKey(
        verbose_name=_("пользователь"),
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="lists_created",
        blank=True,
        null=True,
        default=None,
    )
    title = models.CharField(
        verbose_name=_("название"),
        max_length=512,
    )
    description = models.TextField(
        verbose_name=_("описание"),
        blank=True,
        null=True,
        default=None,
    )
    is_public = models.BooleanField(
        verbose_name=_("публичный"),
        default=False,
    )
    created = models.DateTimeField(verbose_name=_("создан"), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_("изменен"), auto_now=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = _("список")
        verbose_name_plural = _("списки")

    def __str__(self):
        return self.title


class ListItem(OrderedModel):
    """
    Represents an item of the user-created book list.
    """

    list = models.ForeignKey(
        verbose_name=_("список"),
        to=List,
        on_delete=models.CASCADE,
        related_name="items",
    )
    # TODO: remove field `position`
    position = models.IntegerField(
        verbose_name=_("номер в списке"),
        default=1,
    )
    book = models.ForeignKey(
        verbose_name=_("книга"),
        to=Book,
        on_delete=models.CASCADE,
        related_name="list_items",
    )
    description = models.TextField(
        verbose_name=_("описание"),
        blank=True,
        null=True,
        default=None,
    )
    created = models.DateTimeField(verbose_name=_("создана"), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_("изменена"), auto_now=True)

    class Meta:
        ordering = ["order"]
        verbose_name = _("элемент списка")
        verbose_name_plural = _("элементы списков")

    def __str__(self):
        return "#{position} в {list_title} - {book_title}".format(
            position=self.order,
            list_title=self.list.title,
            book_title=self.book.title,
        )
