from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Reviews(models.Model):
    """Модель отзывов. """
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    pub_date = models.DateField(auto_now_add=True)


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField(max_length=30)
    

class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    category = models.ForeignKey(
        'Category',
        related_name='title',
        on_delete=models.SET_NULL,
    )
    genre = models.ManyToManyField(Genre)
