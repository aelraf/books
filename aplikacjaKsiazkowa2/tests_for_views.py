# -*- coding: utf-8 -*-
# mockowanie: https://www.20tab.com/en/blog/test-python-mocking/
# i to: https://medium.com/kami-people/mocking-for-good-mocking-with-python-and-django-4d05cfda4fa3
# i https://yeraydiazdiaz.medium.com/what-the-mock-cheatsheet-mocking-in-python-6a71db997832
from django.db.models import QuerySet
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


class EmptyListViewTests(TestCase):
    def test_list_response(self):
        response = self.client.get(reverse('aplikacjaKsiazkowa2:lista'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['books_data'], [])


class ListViewTests(TestCase):
    def setUp(self) -> None:
        create_brzechwa()
        create_tolkien()
        create_przechrzta()

    def test_list_with_three_books(self):
        books = Book.objects.all()
        response = self.client.get(reverse('aplikacjaKsiazkowa2:lista'))

        books_count = books.count()
        response_count = response.context['books_data'].count()

        self.assertIsInstance(books, QuerySet)
        self.assertQuerysetEqual(response.context['books_data'], books)
        self.assertEqual(response_count, books_count)

    def test_list_if_the_book_in_response(self):
        response = self.client.get(reverse('aplikacjaKsiazkowa2:lista'))

        hobbit = Book.objects.get(id='2')
        self.assertEqual(response.context['books_data'][1], hobbit)

    def test_list_without_the_book(self):
        response = self.client.get(reverse('aplikacjaKsiazkowa2:lista'))

        new_book = Book.objects.create(
            title="Wilczy pagon",
            author="Admin Przuchta",
            pub_date="2019-11-19",
            isbn="978837234575",
            pages=641,
            cover="https://s.lubimyczytac.pl/upload/books/47000/47695/352x500.jpg",
            language="PL"
        )
        self.assertNotIn(new_book, response.context['books_data'])

    def test_list_choose_date(self):
        response = self.client.get(reverse('aplikacjaKsiazkowa2:lista'))


class BookCreateViewTests(TestCase):
    def test_response(self):
        response = self.client.get(reverse('aplikacjaKsiazkowa2:add_book'))
        self.assertEqual(response.status_code, 200)

