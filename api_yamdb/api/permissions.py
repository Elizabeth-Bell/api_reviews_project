from rest_framework import permissions
from users.models import CustomUser


class IsAdminModeratorAuthor(permissions.BasePermission):
    """Доступ на чтение, только пользователю."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
            or request.user.is_superuser
        )


class IsAdmin(permissions.BasePermission):
    """Полный доступ Админа."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin or
            request.user.is_superuser
        )


class IsAdminOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Внесение изменений только с правом администратора"""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_admin or
                 request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user.is_admin or
            request.user.is_superuser
        )