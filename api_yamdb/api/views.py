from reviews.models import Title
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import TitleSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year') #'category', 'genre'
