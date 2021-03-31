import re

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from .models import Category, Comment, Genre, Review, Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review. """
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    def validate(self, data):
        title_id = self.context.get('view').kwargs.get('title_id')
        author = self.context.get('request').user
        if (self.context.get('request').method == 'POST'
            and Review.objects.filter(title_id=title_id,
                                      author_id=author.id).exists()):
            raise serializers.ValidationError(
                {'detail': 'You have already left a review about this title'})
        return data

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
    slug = serializers.SlugField(
        required=False,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )

    def validate(self, data):
        if 'slug' not in data:
            data['slug'] = re.sub(r'[\W_]+', '', data['name'])
        return data

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'
        validators = [
            UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=['name', 'slug']
            )
        ]


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'
        validators = [
            UniqueTogetherValidator(
                queryset=Genre.objects.all(),
                fields=['name', 'slug']
            )
        ]


class TitleViewSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.FloatField()

    class Meta:
        fields = '__all__'
        model = Title


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())

    class Meta:
        fields = '__all__'
        model = Title
