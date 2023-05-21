from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize


class CustomUser(AbstractUser):
    """
    Custom user model with additional fields.
    """

    profile_image = models.ImageField(
        verbose_name=_("изображение профиля"),
        null=True,
        blank=True,
        upload_to="images/profiles/",
    )
    # NB: from `django-imagekit` docs: ImageSpecFields are virtual — they add no fields to your database and don't
    # require a database.
    profile_image_thumbnail_small = ImageSpecField(
        source="profile_image",
        processors=[SmartResize(width=32, height=32, upscale=True)],
        format="JPEG",
        options={"quality": 100},
    )
    profile_image_thumbnail_large = ImageSpecField(
        source="profile_image",
        processors=[SmartResize(width=300, height=300, upscale=True)],
        format="JPEG",
        options={"quality": 100},
    )

    def __str__(self):
        return self.username
