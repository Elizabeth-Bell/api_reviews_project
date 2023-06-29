from django.db import models


class Genre(models.Model):
    name = models.TextField(max_length=256, verbose_name='Название жанра')
    slug = models.SlugField(max_length=50, verbose_name='Слаг жанра',
                            unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(models.Model):
    pass


class Title(models.Model):
    name = models.TextField(max_length=256, verbose_name='Название')
    year = models.IntegerField(verbose_name='Год выпуска')
    description = models.TextField(blank=True, verbose_name='Описание')
    genres = models.ManyToManyField(Genre, through='TitleGenres',
                                   verbose_name='Slug жанра')
    #category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 #related_name='titles',
                                 #verbose_name='Slug категории'
                                 #)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:20]


class TitleGenres(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            'genre', 'title'
        ]

    def __str__(self):
        return f'{self.genre} {self.title}'
