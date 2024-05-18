from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedModel
from apps.users.managers import UserManager


class User(AbstractUser, TimeStampedModel):
    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
