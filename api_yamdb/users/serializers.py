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


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ("username", "confirmation_code")
        model = CustomUser
