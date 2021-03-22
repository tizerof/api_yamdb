from api.models import Review
from rest_framework import serializers


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review. """
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')
    # title = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
