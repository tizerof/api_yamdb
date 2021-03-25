from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination

from api.models import Review, Title, Category

from .permissions import IsAdmin, IsModerator, IsOwner
from .serializers import CommentSerializer, ReviewSerializer, CategorySerializer

PERMISSION_CLASSES = (IsAuthenticatedOrReadOnly, IsOwner, IsAdmin, IsModerator)


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс взаимодействия с моделью Review. """
    serializer_class = ReviewSerializer
    permission_classes = PERMISSION_CLASSES

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
    permission_classes = PERMISSION_CLASSES

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
    permission_classes = (IsAuthenticatedOrReadOnly,)
