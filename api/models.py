from django.db import models
from django.db.models.deletion import CASCADE

from authentication.models import User


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров."""
    name = models.CharField(max_length=30, unique=True,)
    slug = models.SlugField(max_length=30, unique=True,)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(max_length=50)
    year = models.DateField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_NULL
    )
    genre = models.ManyToManyField(Genre)
    author = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


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
