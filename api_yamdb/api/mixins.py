from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters

from .permissions import IsAdminOrReadOnly


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Mixin для жанров и категорий, ограничивающий методы запросов"""
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    search_fields = ('name',)
