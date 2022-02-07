# -*- coding: utf-8 -*-
# każdy model ma osobny serializer - więc u nas jeden wystarczy

from .models import Book
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

