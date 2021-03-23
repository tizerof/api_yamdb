from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    CHOICES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )
    role = models.CharField(max_length=100, choices=CHOICES, default='user')
    bio = models.TextField(max_length=3000, blank=True, null=True)


class UserConfirmation(models.Model):
    email = models.EmailField(max_length=254, blank=False, null=False, unique=True)
    confirmation_code = models.CharField(max_length=1000, blank=True, null=True)
