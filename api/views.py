from django.db.models import Avg
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import SAFE_METHODS
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .filters import TitleFilterSet
from .models import Category, Genre, Review, Title
from .permissions import IsAdmin, IsModerator, IsOwner
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitlePostSerializer, TitleViewSerializer)

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
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateDelListViewset):
    """Класс взаимодействия с моделью Genre. """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdmin,)
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    """Класс взаимодействия с моделью Title. """
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')).order_by('name')
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)
    filterset_class = TitleFilterSet

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleViewSerializer
        return TitlePostSerializer
