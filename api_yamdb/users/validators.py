import re

from django.core.exceptions import ValidationError


def validate_username(username):
    if username.lower() == 'me':
        raise ValidationError('Имя пользователя "me" запрещено!')
    if not re.match(r"^[\w.@+-]+$", username):
        raise ValidationError('Некорректный формат логина')
