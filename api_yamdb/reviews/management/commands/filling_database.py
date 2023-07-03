from django.core.management.base import BaseCommand

import csv

from reviews.models import (Title, Genre, Category,
                            Comment, Review, TitleGenres)
from users.models import CustomUser

PATH = {
    Category: 'static/data/category.csv',
    Comment: 'static/data/comments.csv',
    Genre: 'static/data/genre.csv',
    TitleGenres: 'static/data/genre_title.csv',
    Review: 'static/data/review.csv',
    Title: 'static/data/titles.csv',
    CustomUser: 'static/data/users.csv',
}


class Command(BaseCommand):

    def handle(self, *args, **options):
        for model, path in PATH.items():
            with open(path, mode='r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                model.objects.bulk_create(model(**data) for data in csv_reader)
        self.stdout.write(self.style.SUCCESS('База данных заполнена'))
