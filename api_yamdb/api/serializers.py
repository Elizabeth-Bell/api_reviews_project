from reviews.models import Title, Genre, TitleGenres

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)

    class Meta:
        fields = ('name', 'year', 'description', 'genres')  #'category'
        model = Title

    def create(self, validated_data):
        genres = validated_data.pop('genres')
        title = Title.objects.create(**validated_data)

        for genre in genres:
            current_genre, status = Genre.objects.get_or_create(**genre)
            TitleGenres.objects.create(
                genre=current_genre, title=title
            )
        return title
