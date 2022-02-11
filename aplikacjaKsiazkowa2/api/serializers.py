# -*- coding: utf-8 -*-
"""
Klasa serializująca obiekt QuerySet i zwracająca JSONa
"""

from rest_framework import serializers
from aplikacjaKsiazkowa2.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
