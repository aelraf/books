# -*- coding: utf-8 -*-

from django.db.models import QuerySet
from django.test import TestCase
from django.urls import reverse

from aplikacjaKsiazkowa2.models import Book
from aplikacjaKsiazkowa2.tests_for_views import create_brzechwa, create_przechrzta, create_tolkien


class RESTApiTest(TestCase):
    def setUp(self) -> None:
        create_brzechwa()
        create_tolkien()
        create_przechrzta()

    def test_my_api_without_params(self):
        self.assertEqual(1, 1)

    def test_my_api_with_params(self):
        self.assertEqual(1, 1)

