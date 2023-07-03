from reviews.models import Title, Genre, TitleGenres

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genres = SlugRelatedField(many=True, slug_field='slug', queryset=Genre.objects.all())

    class Meta:
        fields = ('name', 'year', 'description', 'genres')  #'category'
        model = Title
