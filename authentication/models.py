from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user', _('user')
        MODERATOR = 'moderator', _('moderator')
        ADMIN = 'admin', _('admin')

    email = models.EmailField(unique=True, blank=False, null=False)
    role = models.CharField(max_length=100, choices=Roles.choices, default=Roles.USER)
    bio = models.TextField(max_length=3000, blank=True, null=True)

    def is_upperclass(self):
        return self.role in {
            self.Roles.USER,
            self.Roles.MODERATOR,
            self.Roles.ADMIN,
        }


class UserConfirmation(models.Model):
    email = models.EmailField(max_length=254, blank=False, null=False, unique=True)
    confirmation_code = models.CharField(max_length=1000, blank=True, null=True)
