from rest_framework import serializers

from .models import CustomUser


class SignUpSerializer(serializers.ModelSerializer):
    """Сериалайзер для регистрации пользователя"""
    class Meta:
        fields = ('username',
                  'email',
                  )
        model = CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для списка пользователей"""
    role = serializers.ChoiceField(choices=CustomUser.USER_ROLE_CHOICES,
                                   default='user')

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = CustomUser

    def validate_username(self, value):
        """Валидатор юзернейма, имя 'me' запрещено"""
        if value.casefold() == 'me':
            raise serializers.ValidationError('Такое имя запрещено')
        return value


class AboutSerializer(UserSerializer):
    """Сериалайзер для просмотра инфо о пользователе"""
    role = serializers.ChoiceField(choices=CustomUser.USER_ROLE_CHOICES,
                                   read_only=True)


class TokenSerializer(serializers.Serializer):
    """Сериалайзер токена"""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'confirmation_code')
        model = CustomUser
