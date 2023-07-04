from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, generics, pagination, permissions, status,
                            viewsets, mixins)
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

from .mixins import BaseListCreateDestroyMixin
from users.models import CustomUser
from reviews.models import (Category, Genre, Title, Review,
                            Comment)
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsUserAdminModeratorOrReadOnly)
from .serializers import (AboutSerializer, CreateUserSerializer,
                          TokenSerializer, UserSerializer,
                          CategorySerializer, GenreSerializer,
                          TitlePostSerializer, TitleReadSerializer,
                          ReviewSerializer, CommentsSerializer)
from .filters import TitleFilter
from .pagination import Pagination

from rest_framework.permissions import IsAuthenticatedOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"
    lookup_url_kwarg = "username"
    pagination_class = pagination.LimitOffsetPagination
    http_method_names = ("get", "post", "patch", "delete")

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=[permissions.IsAuthenticated],
        url_path="me",
    )
    def me_about(self, request):
        user = request.user
        if request.method == "PATCH":
            serializer = AboutSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        serializer = self.get_serializer(user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class CreateUserView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        username = serializer.validated_data.get("username")
        user, created = CustomUser.objects.get_or_create(
            email=email, username=username)
        confirantion_code = default_token_generator.make_token(user)
        send_mail(
            subject="Register on site YaMDb",
            message=("Код регистрации: " + confirantion_code),
            from_email=None,
            recipient_list=[email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def crate_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = serializer.validated_data.get("confirmation_code")
    user = get_object_or_404(
        CustomUser, username=serializer.validated_data.get("username")
    )
    if default_token_generator.check_token(user, confirmation_code):
        token = str(AccessToken.for_user(user))
        return Response(
            {"acces_token": token},
            status=status.HTTP_200_OK,
        )
    return Response("Не верный токен", status=status.HTTP_400_BAD_REQUEST)


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
