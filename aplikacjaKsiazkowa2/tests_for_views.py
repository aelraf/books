# -*- coding: utf-8 -*-
# mockowanie: https://www.20tab.com/en/blog/test-python-mocking/
# i to: https://medium.com/kami-people/mocking-for-good-mocking-with-python-and-django-4d05cfda4fa3
# i https://yeraydiazdiaz.medium.com/what-the-mock-cheatsheet-mocking-in-python-6a71db997832
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.test import TestCase
from django.urls import reverse

from aplikacjaKsiazkowa2.models import Book
from aplikacjaKsiazkowa2.views import BookCreateView


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

    # def test_list_choose_date(self):
    #     response = self.client.get(reverse('aplikacjaKsiazkowa2:lista'))


class BookCreateViewTests(TestCase):
    def test_add_book_response(self):
        response = self.client.get(reverse('aplikacjaKsiazkowa2:add_book'))
        self.assertEqual(response.status_code, 200)

    def test_add_book_post_with_data(self):
        book = {
            'title': 'Siedem lat chudych',
            'author': "Marian Hemar",
            'pub_date': '2015-01-01',
            'isbn': '9788375654332',
            'pages': 424,
            'cover': 'https://s.lubimyczytac.pl/upload/books/276000/276483/449275-352x500.jpg',
            'language': 'pl'
        }
        response = self.client.post(reverse('aplikacjaKsiazkowa2:add_book'), book)

        self.assertEqual(response.status_code, 302)
        self.assertIs(Book.objects.filter(title=book['title']).exists(), True)

    def test_add_book_with_count_response(self):
        book = {
            'title': 'Siedem lat chudych',
            'author': "Marian Hemar",
            'pub_date': '2015-01-01',
            'isbn': '9788375654332',
            'pages': 424,
            'cover': 'https://s.lubimyczytac.pl/upload/books/276000/276483/449275-352x500.jpg',
            'language': 'pl'
        }
        response = self.client.post(reverse('aplikacjaKsiazkowa2:add_book'), book)

        books = Book.objects.all()
        books_count = books.count()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(1, books_count)

    def test_add_book_with_bad_data(self):
        book = {
            'title': 12345,
            'author': "Mikołaj Gogol Jan Kowalski Edward Nowak",
            'pub_date': '01-12-3456',
            'isbn': '9788375654332',
            'pages': '424',
            'cover': 'qwer1234',
            'language': 'pl'
        }
        response = self.client.post(reverse('aplikacjaKsiazkowa2:add_book'), book)
        self.assertEqual(response.status_code, 302)

        # self.assertRaises(ValidationError, BookCreateView.post, kwargs=book)


class BookDeleteViewTest(TestCase):
    def setUp(self) -> None:
        create_brzechwa()
        create_tolkien()
        create_przechrzta()

    def test_delete_book_response(self):
        response = self.client.get(reverse('aplikacjaKsiazkowa2:delete_book', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_delete_book_with_good_id(self):
        url = reverse('aplikacjaKsiazkowa2:delete_book', kwargs={'pk': 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        books = Book.objects.all()
        books_count = books.count()

        delete_book = Book.objects.get(pk=1)
        response_ok = self.client.post(url)

        self.assertNotIn(delete_book, books)
        # przekierowuje nas do 'listy', więc dlatego status kodu 302
        self.assertEqual(response_ok.status_code, 302)

        books_after_delete = Book.objects.all()
        count_after_delete = books_after_delete.count()

        self.assertGreaterEqual(books_count, count_after_delete)
        self.assertEqual(books_count, count_after_delete + 1)

    def test_delete_book_with_bad_id(self):
        url = reverse('aplikacjaKsiazkowa2:delete_book', kwargs={'pk': 100})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)


class BookUpdateViewTests(TestCase):
    def setUp(self) -> None:
        create_brzechwa()
        create_tolkien()
        create_przechrzta()

    def test_update_book_response(self):
        url = reverse('aplikacjaKsiazkowa2:edit_book', kwargs={'pk': 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_update_book_with_good_id_and_data(self):
        pass
