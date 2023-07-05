import re

from django.conf import settings
from django.shortcuts import get_object_or_404
from reviews.models import (Title, Genre, Category,
                            Comment, Review,
                            TitleGenres)

from django.utils import timezone
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from users.models import CustomUser


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=CustomUser.USER_ROLE_CHOICES,
                                   default="user")

    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = CustomUser

    def validate_username(self, value):
        if value.casefold() == "me":
            raise serializers.ValidationError("Такое имя запрещено")
        return value


class AboutSerializer(UserSerializer):
    role = serializers.ChoiceField(choices=CustomUser.USER_ROLE_CHOICES,
                                   read_only=True)


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=254)

    def validate_username(self, value):
        username = value
        email = self.initial_data.get("email")
        user = CustomUser.objects.filter(username=username).exists()
        user_email = CustomUser.objects.filter(email=email).exists()
        if username.casefold() == "me":
            raise serializers.ValidationError("Такое имя запрещено")
        if not re.match(r"^[\w.@+-]+$", username):
            raise serializers.ValidationError("Не корректный формал логина")
        if user and not user_email:
            raise serializers.ValidationError(
                "Не верная почта для этого пользователя",
            )
        if user_email and not user:
            raise serializers.ValidationError(
                "Пользователь с такой почтой уже существует"
            )
        if user and user_email:
            if CustomUser.objects.filter(username=username,
                                         email=email).exists():
                return value
            raise serializers.ValidationError(
                "Такая почта или имя пользователя существует"
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ("username", "confirmation_code")
        model = CustomUser


class TitleSerializer(serializers.ModelSerializer):
    genres = SlugRelatedField(many=True, slug_field='slug', queryset=Genre.objects.all())
    categories = SlugRelatedField(slug_field='slug', queryset=Category.objects.all())
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    def validate_score(self, value):
        if not settings.MIN_SCORE_VALUE <= value <= settings.MAX_SCORE_VALUE:
            raise serializers.ValidationError(
                f'Оценка должна быть от {settings.MIN_SCORE_VALUE}'
                f'до {settings.MAX_SCORE_VALUE}!',
            )
        return value

    def validate(self, data):
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
        fields = '__all__'
        model = Review


class CommentsSerializer(serializers.ModelSerializer):
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
        fields = '__all__'
        read_only_fields = ('pub_date',)
