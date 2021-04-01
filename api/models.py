from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.deletion import CASCADE

from authentication.models import User

from .validators import title_year_validator


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField(verbose_name='Название', max_length=30)
    slug = models.SlugField(verbose_name='Slug', max_length=30)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров."""
    name = models.CharField(
        verbose_name='Название', max_length=30, unique=True)
    slug = models.SlugField(verbose_name='Slug', max_length=30, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(max_length=50, verbose_name='Название')
    year = models.IntegerField(
        verbose_name='Год',
        blank=True, null=True,
        validators=[title_year_validator])
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_NULL)
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')
    author = models.CharField(
        verbose_name='Автор', max_length=50, blank=True, null=True)
    description = models.TextField(
        verbose_name='Описание', max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзывов. """
    text = models.TextField(verbose_name='Отзыв')
    title = models.ForeignKey(
        Title, verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews')
    author = models.ForeignKey(
        User, verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews')
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateField(
        verbose_name='Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date', 'author',)


class Comment(models.Model):
    """Модель комментариев к отзывам. """
    review = models.ForeignKey(
        Review, verbose_name='Отзыв',
        on_delete=CASCADE,
        related_name='comments')
    text = models.TextField(verbose_name='Комментарий')
    author = models.ForeignKey(
        User, verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comments')
    pub_date = models.DateField(
        verbose_name='Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date', 'author',)
