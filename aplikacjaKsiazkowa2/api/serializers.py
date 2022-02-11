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


class VolumeInfoSerializer(serializers.Serializer):
    pages = serializers.IntegerField(required=False, source="pageCount")


class GugleSerializer(serializers.Serializer):
    volumeInfo = VolumeInfoSerializer()

    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        return value["volumeInfo"]
