from api.models import Review, Title
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets

from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс взаимодействия с моделью Review. """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        """Получение списка комментариев к посту. """
        title = get_object_or_404(Title, pk=self.kwargs.get('post_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        """Сохранение комментария в бд. """
        serializer.save(
            author=self.request.user,
            title_id=self.kwargs.get('title_id'))
