from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    CHOICES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )
    username = models.CharField(max_length=100, blank=True, null=True, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=100, choices=CHOICES, default='user')
    bio = models.TextField(max_length=3000, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email


class UserConfirmation(models.Model):
    email = models.EmailField(max_length=254, blank=False, null=False, unique=True)
    confirmation_code = models.CharField(max_length=1000, blank=False, null=False)
