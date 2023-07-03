from django.contrib import admin

from .models import Category, Genre, Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'display_genre') #'category'
    search_fields = ('name', 'description',)
    list_filter = ('category', 'year')
    empty_value_display = '-пусто-'
    
    def display_genre(self, obj):
        genre_names = obj.genre.values_list("name", flat=True)
        return ", ".join(genre_names)
      
    display_genre.short_description = "Жанр"

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'