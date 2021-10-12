# -*- coding: utf-8 -*-
# każdy model ma osobny serializer - więc u nas jeden wystarczy

from .models import Book
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'pub_date', 'isbn', 'pages', 'cover', 'language']


'''
pierwsze podejście z tutoriala

class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    author = serializers.CharField(max_length=200)
    pub_date = serializers.DateField('data publikacji')
    isbn = serializers.CharField(max_length=15)
    pages = serializers.IntegerField()
    cover = serializers.CharField(max_length=200)
    language = serializers.CharField(max_length=5)

    def create(self, validated_data):
        """
        tworzy i zwraca nową instancję książek, daną w validated_data
        """
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        aktualizuje i zwraca istniejące instancje ksiażek, danych w validated_data
        """
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.pub_date = validated_data.get('pub_date', instance.pub_date)
        instance.isbn = validated_data.get('isbn', instance.isbn)
        instance.pages = validated_data.get('pages', instance.pages)
        instance.cover = validated_data.get('cover', instance.cover)
        instance.language = validated_data.get('language', instance.language)
        instance.save()
        return instance
'''
