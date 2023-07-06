from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, generics, pagination, permissions, status,
                            viewsets)
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from users.models import CustomUser
from reviews.models import (Category, Genre, Title, Review,
                            Comment)
from api.permissions import (IsAdmin, IsAdminOrReadOnly, IsAdminModeratorAuthor)
from users.serializers import (UserSerializer, AboutSerializer, CreateUserSerializer, TokenSerializer,
                               SignUpSerializer)

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


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    username = serializer.validated_data.get('username')
    user = get_object_or_404(CustomUser, username=username)
    email = serializer.validated_data.get('email')
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject="Register on site YaMDb",
        message=("Код регистрации: " + confirmation_code),
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

