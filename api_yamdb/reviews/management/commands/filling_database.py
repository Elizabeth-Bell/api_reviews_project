import csv

from django.core.management.base import BaseCommand
from reviews.models import (Title, Genre, Category,
                            Comment, Review, TitleGenres)
from users.models import CustomUser

SIMPLE_PATH = {
    Category: 'static/data/category.csv',
    Genre: 'static/data/genre.csv',
    CustomUser: 'static/data/users.csv',
}

DIFFICULT_PATH = {
    Title: 'static/data/titles.csv',
    TitleGenres: 'static/data/genre_title.csv',
    Review: 'static/data/review.csv',
    Comment: 'static/data/comments.csv',
}


def category_genre_user_import():
    """Функция для распаковки и создания объектов без полей ForeignKey"""
    for model, path in SIMPLE_PATH.items():
        with open(path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            model.objects.bulk_create(model(**data) for data in csv_reader)


def other_import():
    """Функция для распаковки и создания объектов с полями ForeignKey"""
    for model, path in DIFFICULT_PATH.items():
        with open(path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            if model == Title:
                for row in csv_reader:
                    model.objects.create(
                        id=row['id'],
                        name=row['name'],
                        year=int(row['year']),
                        category=Category.objects.get(id=row['category']),
                    )
            elif model == TitleGenres:
                for row in csv_reader:
                    model.objects.create(
                        id=row['id'],
                        title=Title.objects.get(id=row['title_id']),
                        genre=Genre.objects.get(id=row['genre_id']),
                    )
            elif model == Review:
                for row in csv_reader:
                    model.objects.create(
                        id=row['id'],
                        title=Title.objects.get(id=row['title_id']),
                        text=row['text'],
                        author=CustomUser.objects.get(id=row['author']),
                        score=row['score'],
                        pub_date=row['pub_date'],
                    )
            else:
                for row in csv_reader:
                    model.objects.create(
                        id=row['id'],
                        review=Review.objects.get(id=row['review_id']),
                        text=row['text'],
                        author=CustomUser.objects.get(id=row['author']),
                        pub_date=row['pub_date'],
                    )


class Command(BaseCommand):
    """Создание команды для выполнения импорта csv-файла"""

    def handle(self, *args, **options):
        category_genre_user_import()
        other_import()
        self.stdout.write(self.style.SUCCESS('База данных заполнена'))
