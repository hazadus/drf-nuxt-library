from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


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

    def __str__(self):
        return self.username
