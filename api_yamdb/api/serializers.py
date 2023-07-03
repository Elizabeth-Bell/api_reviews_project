from reviews.models import Title, Genre, TitleGenres, Category

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    genres = SlugRelatedField(many=True, slug_field='slug', queryset=Genre.objects.all())
    categories = SlugRelatedField(slug_field='slug', queryset=Category.objects.all())

    class Meta:
        fields = ('name', 'year', 'description', 'genres', 'categories')
        model = Title
