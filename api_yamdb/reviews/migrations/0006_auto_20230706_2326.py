# Generated by Django 2.2.16 on 2023-07-06 20:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20230706_2311'),
    ]

    operations = [
        migrations.RenameField(
            model_name='title',
            old_name='genres',
            new_name='genre',
        ),
    ]