import os

from django.db.models import Avg
from rest_framework import serializers, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.models import Category, Genre, Review, Title

from .filters import CategoryFilterSet, GenreFilterSet, TitleFilterSet
from .permissions import (IsActiveUserPermission, IsAdmin, IsAdminOrReadOnly,
                          IsModerator, IsOwner)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)

REVIEW_COMMENT_PERMISSION = (IsOwner | IsModerator | IsAdmin,)


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс взаимодействия с моделью Review. """
    serializer_class = ReviewSerializer
    permission_classes = REVIEW_COMMENT_PERMISSION

    def get_queryset(self):
        """Получение списка отзывов. """
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        """Сохранение отзыва в бд. """
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = REVIEW_COMMENT_PERMISSION

    def get_queryset(self):
        """Получение списка комментариев к отзыву. """
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        """Сохранение комментария в бд. """
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post', 'delete']
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filterset_class = CategoryFilterSet


class GenreViewSet(CategoryViewSet):
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    filterset_class = GenreFilterSet


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().order_by('id').annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilterSet

    def prepare_category_and_genre(self):
        data = {}
        if self.request.data.get('category'):
            category_slug = self.request.data.get('category')
            assigned_category = Category.objects.get(slug=category_slug)
            data['category'] = assigned_category
        if self.request.data.get('genre'):
            input_slug = self.request.data.get('genre')
            input_slug = input_slug.replace(' ', '')
            genre_slug_list = input_slug.split(',')
            assigned_genre_queryset = []
            for genre_slug in genre_slug_list:
                try:
                    found_genre = Genre.objects.get(slug=genre_slug)
                except Genre.DoesNotExist:
                    found_genre = None
                assigned_genre_queryset.append(found_genre)
            data['genre'] = assigned_genre_queryset
        return data

    def perform_create(self, serializer):
        data = self.prepare_category_and_genre()
        serializer.is_valid()
        serializer.save(**data)

    def perform_update(self, serializer):
        data = self.prepare_category_and_genre()
        serializer.is_valid()
        serializer.save(**data)
