from django.contrib import admin

from .models import Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description') #'genre', 'category'
    search_fields = ('name', 'description',)
    empty_value_display = '-пусто-'
