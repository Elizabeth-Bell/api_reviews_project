import re

from django.utils import timezone
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser


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
