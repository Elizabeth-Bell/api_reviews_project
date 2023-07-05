from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUserManager(BaseUserManager):

    def create_user(self, email, username, role='', bio='', password=None):
        if not email:
            raise ValueError('e-mail обязателен для регистрации')
        if not username:
            raise ValueError('username обязателен для регистрации')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username
            bio=bio,
            role=role
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, email, username, password):
        return self._create_user(email, username, password, is_staff=True, is_superuser=True)

    
class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    CHOICES_ROLE = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )
    username = models.CharField(
        'Логин',
        max_length=100,
        unique=True,
    )
    first_name = models.CharField(
        'Имя', max_length=100, blank=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль пользователя',
        default=USER,
        max_length=40,
        choices=CHOICES_ROLE)
    email = models.EmailField('E-mail пользователя',
                              unique=True, max_length=40)
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=100,
        null=True
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    def __str__(self):
        return self.username
