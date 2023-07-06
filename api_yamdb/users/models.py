from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .validators import validate_username


class CustomUserManager(BaseUserManager):
    """Кастомный менеджер"""

    def create_user(self, email, username, role='', bio='', password=None):
        """Функция создания юзера"""
        if not email:
            raise ValueError('e-mail обязателен для регистрации')
        if not username:
            raise ValueError('username обязателен для регистрации')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            bio=bio,
            role=role
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self, email, username, password, role='admin', bio=''
    ):
        """Функция создания суперюзера"""
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.role = role
        user.bio = bio
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель юзера"""
    ADMINISTRATOR = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    USER_ROLE_CHOICES = [
        (ADMINISTRATOR, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    ]
    is_active = models.BooleanField(default=True,
                                    verbose_name='Активный')
    is_staff = models.BooleanField(default=False,
                                   verbose_name='Стафф')
    is_superuser = models.BooleanField(default=False,
                                       verbose_name='Суперпользователь')
    username = models.CharField(
        verbose_name='имя пользователя',
        max_length=150,
        unique=True,
        validators=[validate_username, ]
    )
    first_name = models.CharField(max_length=150, blank=True,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=150, blank=True,
                                 verbose_name='Фамилия')
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='email'
    )

    bio = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    role = models.CharField(
        max_length=50,
        choices=USER_ROLE_CHOICES,
        default='user',
        verbose_name='роль'
    )
    date_joined = models.DateTimeField(
        verbose_name='дата создания',
        auto_now_add=True
    )
    confirmation_code = models.CharField(
        blank=True,
        verbose_name='Код для авторизации',
        max_length=39,
    )
    last_login = models.DateTimeField(
        verbose_name='последний вход в систему',
        auto_now=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_short_name(self):
        return self.username

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return (self.role == self.ADMINISTRATOR
                or self.is_superuser)

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
