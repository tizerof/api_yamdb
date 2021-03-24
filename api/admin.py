from django.contrib import admin

from .models import Category, Genre, Title

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    empty_value_display = '-empty-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    empty_value_display = '-empty-'


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category', 'author', 'description')
    search_fields = ('description',)
    list_filter = ('name',)
    empty_value_display = '-empty-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
