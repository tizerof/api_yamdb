from django.db import models


class Users(models.Model):
    CHOICES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )
    username = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=254, blank=False, null=False)
    role = models.CharField(max_length=100, choices=CHOICES, default='user')
    description = models.TextField(max_length=3000, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)


class UserConfirmation(models.Model):
    email = models.EmailField(max_length=254, blank=False, null=False, unique=True)
    confirmation_code = models.CharField(max_length=1000, blank=False, null=False)

