# -*- coding: utf-8 -*-
"""
Klasa serializująca obiekt QuerySet i zwracająca JSONa
"""

from rest_framework.serializers import ModelSerializer
from aplikacjaKsiazkowa2.models import Book


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

