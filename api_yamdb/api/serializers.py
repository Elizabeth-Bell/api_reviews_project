from reviews.models import Title

from rest_framework import serializers


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'year', 'description') #'genre', 'category'
        model = Title
