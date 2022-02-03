# -*- coding: utf-8 -*-

from django.test import TestCase
from django.urls import reverse

from aplikacjaKsiazkowa2.models import Book


def create_brzechwa():
    return Book.objects.create(
        title="Brzechwa dzieciom",
        author="Jan Brzechwa",
        pub_date="2011-01-01",
        isbn="53387501243KS",
        pages=136,
        cover="https://bigimg.taniaksiazka.pl/images/popups/607/53387501243KS.jpg",
        language="PL"
    )


def create_tolkien():
    return Book.objects.create(
        title="Hobbit, czyli tam i z powrotem",
        author="John Tolkien",
        pub_date="2002-02-19",
        isbn="8320716810",
        pages=314,
        cover="https://s.lubimyczytac.pl/upload/books/4000/4966/352x500.jpg",
        language="PL"
    )


def create_przechrzta():
    return Book.objects.create(
        title="Wilczy legion",
        author="Adam Przechrzta",
        pub_date="2009-10-09",
        isbn="9788375741575",
        pages=416,
        cover="https://s.lubimyczytac.pl/upload/books/47000/47695/352x500.jpg",
        language="PL"
    )


"""
class BookUpdateViewTests(TestCase):
    def test_update_book_get(self):
        book = create_brzechwa()

        response = self.client.get(reverse('aplikacjaKsiazkowa2:edit_book', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_update_book_post(self):
        book = create_brzechwa()

        url = reverse('aplikacjaKsiazkowa2:edit_book',  kwargs={'id': 1})
        response = self.client.post(url, {
            'title': "Brzechwa misiom i innym",
            'author': book.author,
            'pub_date': book.pub_date,
            'isbn': book.isbn,
            'pages': book.pages,
            'cover': book.cover,
            'language': book.language
        })
        self.assertEqual(response.status_code, 200)"""


class IndexViewTests(TestCase):
    def test_index_response(self):
        response = self.client.get(reverse('aplikacjaKsiazkowa2:index'))
        self.assertEqual(response.status_code, 200)


class ListViewTests(TestCase):
    def test_list_response(self):
        response = self.client.get(reverse('aplikacjaKsiazkowa2:lista'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['books_data'], [])

    def setUp(self) -> None:
        create_brzechwa()
        create_tolkien()

    def test_list_with_one_book(self):
        books = Book.objects.all()
        response = self.client.get(reverse('aplikacjaKsiazkowa2:lista'))

        self.assertQuerysetEqual(response.context['books_data'], books)


"""
class BookCreateViewTests(TestCase):
    def test_response(self):
        response = self.client.get(reverse('aplikacjaKsiazkowa2:add_book'))
        self.assertEqual(response.status_code, 200)
"""
