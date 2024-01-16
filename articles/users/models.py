from collections.abc import Iterable

from django.contrib.auth.models import AbstractUser
from django.db import models

from users.tasks import resize_user_avatar


class User(AbstractUser):
    photo = models.ImageField(
        upload_to="users/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография"
    )
    date_birth = models.DateTimeField(
        blank=True, null=True, verbose_name="Дата рождения"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            resize_user_avatar.delay(self.photo.path)
