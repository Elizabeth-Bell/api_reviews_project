from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (signup, UserViewSet, crate_token)

app_name = 'users'

v1_router = DefaultRouter()

v1_router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', crate_token, name='get_token'),
    path('', include(v1_router.urls)),
]
