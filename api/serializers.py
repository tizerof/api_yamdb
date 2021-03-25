from rest_framework import serializers

from api.models import Comment, Review, Category, Genre


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review. """
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели Category. """

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели Genre. """

    class Meta:
        model = Genre
        fields = ('name', 'slug')
