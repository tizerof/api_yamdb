from django.db import models
from django.db.models.deletion import CASCADE

from authentication.models import User


class Title(models.Model):
    pass


class Review(models.Model):
    """Модель отзывов. """
    CHOICES = ((i, i) for i in range(1, 11))
    text = models.TextField()
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(choices=CHOICES)
    pub_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date', 'author',)


class Comment(models.Model):
    """Модель комментариев к отзывам. """
    review = models.ForeignKey(
        Review, on_delete=CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date', 'author',)
