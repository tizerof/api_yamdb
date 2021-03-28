from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user', _('user')
        MODERATOR = 'moderator', _('moderator')
        ADMIN = 'admin', _('admin')

    """ 
    Валидатор нужен чтобы в username не было символов вроде '@'
    которые не обработаются в /users/{username}/
    """
    alphanumeric = RegexValidator(
        r'^[0-9a-zA-Z_]*$',
        'Разрешены символы алфавита, цифры и нижние подчеркивания.'
    )

    username = models.CharField(max_length=50, unique=True,
                                blank=True, null=True,
                                validators=[alphanumeric])
    email = models.EmailField(unique=True, blank=False, null=False)
    role = models.CharField(max_length=100, choices=Roles.choices, default=Roles.USER)
    bio = models.TextField(max_length=3000, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class UserConfirmation(models.Model):
    """
    Хранит данные о подтверждении email
    """
    email = models.EmailField(max_length=254, blank=False, null=False, unique=True)
    confirmation_code = models.CharField(max_length=1000, blank=True, null=True)
