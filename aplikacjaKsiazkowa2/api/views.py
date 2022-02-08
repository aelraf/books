# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
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

        author = request.GET['author'] if 'author' in request.GET else ""
        title = request.GET['title'] if 'title' in request.GET else ""
        language = request.GET['language'] if 'language' in request.GET else ""
        d1 = request.GET['d1'] if 'd1' in request.GET else ""
        d2 = request.GET['d2'] if 'd2' in request.GET else ""

        try:
            if title != "":
                books = Book.objects.filter(title__icontains=title)
                serializer = BookSerializer(books, many=True)
                return Response(serializer.data)
            if author != "":
                books = Book.objects.filter(author__icontains=author)
                serializer = BookSerializer(books, many=True)
                return Response(serializer.data)
            if language != '':
                books = Book.objects.filter(language__icontains=language)
                serializer = BookSerializer(books, many=True)
                return Response(serializer.data)
            if d1 != '' and d2 != '':
                books = Book.objects.filter(pub_date__range=(d1, d2))
                serializer = BookSerializer(books, many=True)
                return Response(serializer.data)
        except ValidationError as err:
            print("BookListApi - ValidationError")
            raise Http404
        except KeyError as err:
            print("BookListApi - KeyError")
            raise Http404
        else:
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data)
