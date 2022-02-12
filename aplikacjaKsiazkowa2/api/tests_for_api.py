# -*- coding: utf-8 -*-
import json

from django.http import Http404
from django.test import TestCase
from rest_framework import status
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

        self.assertEqual(response.status_code, status.HTTP_200_OK)

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

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        self.assertEqual(len(data), 3)

    def test_book_list_api_with_good_title(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/api/books?title=brzechwa')
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        self.assertEqual(len(data), 1)

        books = Book.objects.get(title__icontains='brzechwa')
        self.assertEqual(result[0]['title'], books.title)

    def test_book_list_api_with_bad_title(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/api/books?title=1234')
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        self.assertEqual(len(data), 0)

        self.assertEqual(result, [])

    def test_book_list_api_with_good_author(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/api/books?author=Tolkien')
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        self.assertEqual(len(data), 1)

        books = Book.objects.get(author__icontains='Tolkien')
        self.assertEqual(result[0]['author'], books.author)

    def test_book_list_api_with_bad_author(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/api/books?author=qwe123tre')
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        self.assertEqual(len(data), 0)

        self.assertEqual(result, [])

    def test_book_list_with_good_language(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/api/books?language=pl')
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        self.assertEqual(len(data), 3)

        books = Book.objects.filter(language__icontains='pl')
        self.assertEqual(result[0]['language'], books[0].language)

    def test_book_list_with_non_existing_language(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/api/books?language=eng')
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        self.assertEqual(len(data), 0)

        self.assertEqual(result, [])

    def test_book_list_with_bad_language(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/api/books?language=12qwerty345')
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        self.assertEqual(len(data), 0)

        self.assertEqual(result, [])

    def test_book_list_with_two_good_dates(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/api/books?pub_date_after=2000-01-01&pub_date_before=2020-01-01')
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        self.assertEqual(len(data), 3)

        self.assertGreaterEqual(result[0]['pub_date'], '2000-01-01')
        self.assertLessEqual(result[0]['pub_date'], '2020-01-01')

    def test_book_list_with_one_date(self):
        # zwróci całą listę książek, bo warunek nie będzie spełniony
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/api/books?pub_date_after=2000-01-01')
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        self.assertEqual(len(data), 3)

        self.assertGreaterEqual(result[0]['pub_date'], '1000-01-01')
        self.assertLessEqual(result[0]['pub_date'], '2022-01-01')

    def test_book_list_with_bad_date(self):
        # przy błędnej dacie także zwróci całą listę książek
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/api/books?pub_date_after=ala-ma-kota')
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = json.loads(response.content)
        self.assertEqual(len(data), 1)


class BookDetailApiTests(TestCase):
    def setUp(self) -> None:
        create_brzechwa()
        create_tolkien()
        create_przechrzta()

    def test_get_with_pk(self):
        client = APIClient()
        response = client.get('http://127.0.0.1:8000/api/books/1')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        self.assertEqual(len(data), 8)

    def test_get_with_bad_pk(self):
        client = APIClient()
        response = client.get('http://127.0.0.1:8000/api/books/qwerty')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
