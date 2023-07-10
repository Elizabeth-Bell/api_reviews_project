from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import (filters, pagination, permissions, status,
                            viewsets)
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import (IsAdmin)
from .models import CustomUser
from .serializers import (UserSerializer, AboutSerializer, TokenSerializer,
                          SignUpSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели CustomUser"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    pagination_class = pagination.LimitOffsetPagination
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated],
        url_path='me',
    )
    def me_about(self, request):
        """Функция для изменения информации о себе по отдельному эндпойнту"""
        user = request.user
        if request.method == 'PATCH':
            if not user.is_admin or user.is_superuser:
                serializer = AboutSerializer(user,
                                             data=request.data,
                                             partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK,
                )
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        serializer = self.get_serializer(user)
        if user.role == 'admin':
            UserSerializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


def create_send_confirmation_token(user, email):
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Register on site YaMDb',
        message=('Код регистрации: ' + confirmation_code),
        from_email=None,
        recipient_list=[email],
    )


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    if CustomUser.objects.filter(username=username, email=email).exists():
        user = get_object_or_404(CustomUser, username=username)
        serializer = SignUpSerializer(user, data=request.data, partial=True)
    else:
        serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    create_send_confirmation_token(user=get_object_or_404(CustomUser,
                                                          username=username),
                                   email=email)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def crate_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(
        CustomUser, username=serializer.validated_data.get('username'))
    if default_token_generator.check_token(user, confirmation_code):
        token = str(AccessToken.for_user(user))
        return Response(
            {'access_token': token},
            status=status.HTTP_200_OK)
    return Response('Неверный токен', status=status.HTTP_400_BAD_REQUEST)
