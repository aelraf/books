# -*- coding: utf-8 -*-
import json

from django.http import Http404
from django.test import TestCase
from rest_framework.test import APIClient, RequestsClient

from aplikacjaKsiazkowa2.api.views import BookDetailApi
from aplikacjaKsiazkowa2.models import Book
from aplikacjaKsiazkowa2.tests_for_views import create_brzechwa, create_przechrzta, create_tolkien


class RESTApiTest(TestCase):
    def setUp(self) -> None:
        create_brzechwa()
        create_tolkien()
        create_przechrzta()

    def test_get_api_response(self):
        client = APIClient()
        response = client.get('http://127.0.0.1:8000/api')

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(len(data), 7)


class BookListApiTests(TestCase):
    def setUp(self) -> None:
        create_brzechwa()
        create_tolkien()
        create_przechrzta()

    def test_my_api_books(self):
        client = APIClient()
        response = client.get('http://127.0.0.1:8000/api/books')

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(len(data), 3)

    def test_book_list_api_with_good_title(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/api/books?title=brzechwa')
        result = response.json()

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(len(data), 1)

        books = Book.objects.get(title__icontains='brzechwa')
        self.assertEqual(result[0]['title'], books.title)

    def test_book_list_api_with_bad_title(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/api/books?title=1234')
        result = response.json()

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(len(data), 0)

        self.assertEqual(result, [])

    def test_book_list_api_with_good_author(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/api/books?author=Tolkien')
        result = response.json()

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(len(data), 1)

        books = Book.objects.get(author__icontains='Tolkien')
        self.assertEqual(result[0]['author'], books.author)

    def test_book_list_api_with_bad_author(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/api/books?author=qwe123tre')
        result = response.json()

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(len(data), 0)

        self.assertEqual(result, [])


class BookDetailApiTests(TestCase):
    def setUp(self) -> None:
        create_brzechwa()
        create_tolkien()
        create_przechrzta()

    def test_get_with_pk(self):
        client = APIClient()
        response = client.get('http://127.0.0.1:8000/api/books/1')

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(len(data), 8)

    def test_get_with_bad_pk(self):
        client = APIClient()
        with self.assertRaises(ValueError):
            response = client.get('http://127.0.0.1:8000/api/books/qwerty')
            self.assertEqual(response.status_code, 200)

    def test_get_with_to_big_pk(self):
        client = APIClient()

        response = client.get('http://127.0.0.1:8000/api/books/100')
        self.assertEqual(response.status_code, 404)

    def test_get_object_with_good_pk(self):
        pk = 2
        book_detail = BookDetailApi()
        book = book_detail.get_object(pk=pk)

        assert book.author == "John Tolkien"

    def test_get_object_with_bad_pk(self):
        pk = 123
        book_detail = BookDetailApi()

        self.assertRaises(Http404, book_detail.get_object, pk=pk)
