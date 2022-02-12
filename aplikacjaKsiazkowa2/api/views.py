# -*- coding: utf-8 -*-
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from aplikacjaKsiazkowa2.models import Book
from .filters import BookFilter
from .serializers import BookSerializer


class GetRoutesApi(APIView):
    def get(self, request):
        routes = [
            'GET /api',
            'GET /api/books',
            'GET /api/books/:id',
            'GET /api/books?title=looking_title',
            'GET /api/books?author=looking_author',
            'GET /api/books?language=looking_language',
            'GET /api/books?pub_date_after=YYYY-MM-DD&pub_date_before=YYYY-MM-DD',
        ]
        return Response(routes)


class BookDetailApi(RetrieveAPIView):
    """
    Wyświetla pojedyncze obiekty, można rozwinąć w kierunku edycji, dodawania i usuwania.
    """
    serializer_class = BookSerializer
    queryset = Book.objects.all()


class BookListApi(ListAPIView):
    """
    Listujemy wszystkie książki, a jeśli dostaniemy paramter wywołania, to filtrujemy wyniki.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilter
