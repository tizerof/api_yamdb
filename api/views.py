from django.db.models import Avg
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .filters import TitleFilterSet
from .models import Category, Genre, Review, Title
from .permissions import IsAdmin, IsModerator, IsOwner
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)

REVIEW_COMMENT_PERMISSION = (IsOwner | IsModerator | IsAdmin,)


class ReviewViewSet(ModelViewSet):
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


class CommentViewSet(ModelViewSet):
    """Класс взаимодействия с моделью Comment. """
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


class CreateDelListViewset(CreateModelMixin, DestroyModelMixin,
                           ListModelMixin, GenericViewSet):
    """Класс с доступом к операциям create, destroy и list. """
    pass


class CategoryViewSet(CreateDelListViewset):
    """Класс взаимодействия с моделью Category. """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateDelListViewset):
    """Класс взаимодействия с моделью Genre. """
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdmin,)
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    """Класс взаимодействия с моделью Title. """
    queryset = Title.objects.all().order_by('id').annotate(
        rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)
    filterset_class = TitleFilterSet

    def prepare_category_and_genre(self):
        """Проверка полей category и genre. """
        data = {}
        if self.request.data.get('category'):
            category_slug = self.request.data.get('category')
            assigned_category = Category.objects.get(slug=category_slug)
            data['category'] = assigned_category
        if self.request.data.get('genre'):
            input_slug = self.request.data.getlist('genre')
            print(self.request.data, ' - ', input_slug)
            assigned_genre_queryset = []
            for genre_slug in input_slug:
                try:
                    found_genre = Genre.objects.get(slug=genre_slug)
                except Genre.DoesNotExist:
                    found_genre = None
                assigned_genre_queryset.append(found_genre)
            data['genre'] = assigned_genre_queryset
        return data

    def perform_create(self, serializer):
        """Сохранение произведения в бд. """
        data = self.prepare_category_and_genre()
        serializer.is_valid()
        serializer.save(**data)

    def perform_update(self, serializer):
        """Обновление данных произведения в бд. """
        data = self.prepare_category_and_genre()
        serializer.is_valid()
        serializer.save(**data)
