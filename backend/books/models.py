from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Tag(models.Model):
    """
    Represents a tag assigned to the book.
    """

    user = models.ForeignKey(
        verbose_name=_("пользователь"),
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="tags",
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
    )
    author = models.ForeignKey(
        verbose_name=_("автор"),
        to=Author,
        on_delete=models.CASCADE,
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
    publisher = models.ForeignKey(
        verbose_name=_("идательство"),
        to=Publisher,
        on_delete=models.CASCADE,
        related_name="books",
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
    profile_image = models.ImageField(
        verbose_name=_("обложка"),
        null=True,
        blank=True,
        upload_to="images/covers/",
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
        return "{book}, {author}".format(
            book=self.title,
            author=self.author,
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
