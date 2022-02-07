# -*- coding: utf-8 -*-
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from aplikacjaKsiazkowa2.models import Book
from .serializers import BookSerializer


@api_view(['GET'])
def get_route(request):
    routes = [
        'GET /api',
        'GET /api/books',
        'GET /api/books/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_book(request, pk):
    book = Book.objects.get(id=pk)
    serializer = BookSerializer(book, many=False)
    return Response(serializer.data)


class BookDetailApi(APIView):
    """
    Wyświetla pojedyncze obiekty, można rozwinąć w kierunku edycji, dodawania i usuwania.
    """
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist as err:
            print("BookDetailApi - get_object: {}".format(err))
            raise Http404

    def get(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)


class BookListApi(APIView):
    """
    Listujemy wszystkie książki, a jeśli dostaniemy paramter wywołania, to filtrujemy wyniki.
    """
    def get(self, request, format=None):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
