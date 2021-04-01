from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user', 'user'
        MODERATOR = 'moderator', 'moderator'
        ADMIN = 'admin', 'admin'

    # Валидатор нужен чтобы в username не было символов вроде '@'
    # которые не обработаются в /users/{username}/
    alphanumeric = RegexValidator(
        r'^[0-9a-zA-Z_]*$',
        'Разрешены символы алфавита, цифры и нижние подчеркивания.'
    )
    username_validator = alphanumeric
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=100, choices=Roles.choices, default=Roles.USER)
    bio = models.TextField(max_length=3000, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class UserConfirmation(models.Model):
    """
    Хранит данные о подтверждении email
    """
    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(
        max_length=1000, blank=True, null=True)
