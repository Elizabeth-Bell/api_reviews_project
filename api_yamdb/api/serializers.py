from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import (Title, Genre, Category,
                            Comment, Review,
                            )


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер жанра"""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер категории"""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения списка произведений"""
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True,
                                      source='reviews__score__avg')

    class Meta:
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', 'rating')
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер для добавления произведений"""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер отзывов"""
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    def validate_score(self, value):
        """Валидация оценки"""
        if not settings.MIN_SCORE_VALUE <= value <= settings.MAX_SCORE_VALUE:
            raise serializers.ValidationError(
                f'Оценка должна быть от {settings.MIN_SCORE_VALUE}'
                f'до {settings.MAX_SCORE_VALUE}!',
            )
        return value

    def validate(self, data):
        """Валидация отзыва"""
        author = self.context['request'].user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if self.instance is None and \
                Review.objects.filter(title=title, author=author).exists():
            raise serializers.ValidationError(
                'Существует только один отзыв',
            )
        return data

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentsSerializer(serializers.ModelSerializer):
    """Сериалайзер комментариев"""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'review', 'author', 'text', 'pub_date')
        read_only_fields = ('pub_date',)
