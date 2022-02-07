# -*- coding: utf-8 -*-
import json

from django.db.models import QuerySet
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory, RequestsClient, APIClient

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
        self.assertEqual(len(data), 3)

    def test_my_api_books(self):
        client = APIClient()
        response = client.get('http://127.0.0.1:8000/api/books')

        self.assertEqual(response.status_code, 200)

    def test_my_api_books_with_pk(self):
        client = APIClient()
        response = client.get('http://127.0.0.1:8000/api/books/1')

        self.assertEqual(response.status_code, 200)
