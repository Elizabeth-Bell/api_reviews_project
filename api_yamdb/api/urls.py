from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TitleViewSet, GenreViewSet, CategoryViewSet


app_name = 'api'

v1_router = DefaultRouter()

v1_router.register('titles', TitleViewSet)
v1_router.register('genres', GenreViewSet)
v1_router.register('categories', CategoryViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
