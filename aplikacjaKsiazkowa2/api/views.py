# -*- coding: utf-8 -*-

from rest_framework.decorators import api_view
from rest_framework.response import Response

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
