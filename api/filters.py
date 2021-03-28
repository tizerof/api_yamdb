from datetime import datetime

from django_filters import rest_framework as filters
from rest_framework import serializers

from .models import Category, Genre, Title


class CategoryFilterSet(filters.FilterSet):
    search = filters.CharFilter(
        method='get_search',
        field_name='name'
    )

    def get_search(self, queryset, field_name, value, ):
        if value:
            filtered_queryset = queryset.filter(name__icontains=value)
            return filtered_queryset
        return queryset

    class Meta:
        model = Category
        fields = ['search']


class GenreFilterSet(CategoryFilterSet):

    class Meta:
        model = Genre
        fields = ['search']


class TitleFilterSet(filters.FilterSet):
    category = filters.CharFilter(method='get_category')
    genre = filters.CharFilter(method='get_genre')
    name = filters.CharFilter(method='get_name')
    year = filters.NumberFilter(method='get_year')

    def get_category(self, queryset, field_name, value, ):
        if value:
            filtered_queryset = queryset.filter(
                category__slug__icontains=value
            )
            return filtered_queryset
        return queryset

    def get_genre(self, queryset, field_name, value, ):
        if value:
            filtered_queryset = queryset.filter(genre__slug__icontains=value)
            return filtered_queryset
        return queryset

    def get_name(self, queryset, field_name, value, ):
        if value:
            filtered_queryset = queryset.filter(name__icontains=value)
            return filtered_queryset
        return queryset

    def get_year(self, queryset, field_name, value, ):
        if value:
            try:
                filtered_queryset = queryset.filter(
                    year=datetime.strptime(str(value), '%Y')
                )
            except ValueError:
                raise serializers.ValidationError('Неправильно указан год.')
            return filtered_queryset
        return queryset

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']
