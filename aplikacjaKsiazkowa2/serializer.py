# -*- coding: utf-8 -*-
# każdy model ma osobny serializer - więc u nas jeden wystarczy

from .models import Book
from rest_framework import serializers


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'pub_date', 'isbn', 'pages', 'cover', 'languague']



