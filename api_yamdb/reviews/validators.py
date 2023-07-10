from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """Валидатор года, не больше текущего"""
    current_year = timezone.now().year
    if value >= current_year:
        raise ValidationError('Год не может быть больше текущего')
    elif value <= settings.MAX_SCORE_VALUE:
        raise ValidationError('Год не может быть отрицательным')
