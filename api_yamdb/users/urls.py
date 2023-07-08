from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import signup, crate_token, UserViewSet

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
urlpatterns = [
    path('', include(router.urls)),
    path(
        'auth/token/', crate_token.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'auth/signup/', signup.as_view(),
        name='sign_up'
    ),
]
