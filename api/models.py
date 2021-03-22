from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Title(models.Model):
    pass


class Review(models.Model):
    """Модель отзывов. """
    text = models.TextField()
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(default=0, null=True, blank=True)
    pub_date = models.DateField(auto_now_add=True)
