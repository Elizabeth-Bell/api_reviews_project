from reviews.models import (Review, Title,
                            Genre, Category)
from rest_framework import filters, viewsets, status, mixins
from django_filters.rest_framework import DjangoFilterBackend
from api.permissions import (IsAdminModeratorAuthorOrReadOnly,
                             IsAdminModeratorAuthorOrReadOnly,
                             )
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import (CommentsSerializer, ReviewSerializer,
                          TitleSerializer, GenreSerializer, CategorySerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Review"""
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminModeratorAuthorOrReadOnly,
    )

    def title_get_or_404(self):
        return get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))

    def get_queryset(self):
        title = self.title_get_or_404()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.title_get_or_404()
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, title=title)
        return Response(status=status.HTTP_201_CREATED)
    

class CommentsViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Comments"""
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAdminModeratorAuthorOrReadOnly,)

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
      

class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'genres__slug', 'categories__slug')


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
