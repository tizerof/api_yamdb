import os
import re

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from api.models import Category, Comment, Genre, Review, Title


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
    slug = serializers.SlugField(
        required=False,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )

    def validate(self, data):
        os.system('clear')
        print('CATEGORY SERIALIZER IS BEING VALIDATED!!!1111')
        print(data)
        input()

        if 'slug' not in data:
            data['slug'] = re.sub(r'[\W_]+', '', data['name'])
            os.system('clear')
            print(data)
            print(data['slug'])
            input()
        return data

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'
        validators = [
            UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=['name', 'slug']
            )
        ]


class GenreSerializer(CategorySerializer):
    """ Сериализатор модели Genre. """
    slug = serializers.SlugField(
        required=False,
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'
        validators = [
            UniqueTogetherValidator(
                queryset=Genre.objects.all(),
                fields=['name', 'slug']
            )
        ]


class TitleSerializer(serializers.ModelSerializer):
    """ Сериализатор модели Title. """
    genre = GenreSerializer(many=True, required=False, read_only=True)
    category = CategorySerializer(required=False, read_only=True)
    rating = serializers.DecimalField(
        max_digits=3,
        decimal_places=1,
        required=False
    )
    year = serializers.DateField(
        format='%Y',
        input_formats=['%Y'],
        required=False
    )
    description = serializers.CharField(required=False)
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=Title.objects.all())]
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
