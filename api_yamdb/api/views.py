from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, status,
                            viewsets)
from rest_framework.response import Response
from reviews.models import (Category, Genre, Title, Review)

from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import (IsAdminOrReadOnly, IsAdminModeratorAuthor)
from .serializers import (CategorySerializer, GenreSerializer,
                          ReviewSerializer, CommentsSerializer,
                          TitleSerializer, TitleCreateSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Review"""
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthor,)

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        queryset = get_object_or_404(Title, id=title_id)
        return queryset.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        queryset = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=queryset)
        return Response(status=status.HTTP_201_CREATED)


class CommentsViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Comments"""
    serializer_class = CommentsSerializer
    permission_classes = (IsAdminModeratorAuthor,)

    def review_get_or_404(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id'),
        )

    def perform_create(self, serializer):
        review = self.review_get_or_404()
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = self.review_get_or_404()
        return review.comments.all()


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Title"""
    queryset = Title.objects.all().annotate(Avg('reviews__score'))
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ('name', 'year', 'genres', 'category')
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return TitleCreateSerializer
        return TitleSerializer


class GenreViewSet(ListCreateDestroyViewSet):
    """ViewSet для модели Genre"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(ListCreateDestroyViewSet):
    """ViewSet для модели Category"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
