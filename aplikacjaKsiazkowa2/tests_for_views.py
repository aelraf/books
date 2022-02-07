# -*- coding: utf-8 -*-
# mockowanie: https://www.20tab.com/en/blog/test-python-mocking/
# i to: https://medium.com/kami-people/mocking-for-good-mocking-with-python-and-django-4d05cfda4fa3
# i https://yeraydiazdiaz.medium.com/what-the-mock-cheatsheet-mocking-in-python-6a71db997832
# from django.core.exceptions import ValidationError
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


class ListViewChoosingDataTests(TestCase):
    def setUp(self) -> None:
        create_brzechwa()
        create_tolkien()
        create_przechrzta()

    def test_list_post(self):
        url = reverse('aplikacjaKsiazkowa2:lista')
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)

    def test_list_post_with_title(self):
        url = reverse('aplikacjaKsiazkowa2:lista')
        choosen = {'q': 'Hobbit'}
        response = self.client.post(url, choosen)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hobbit")
        self.assertNotContains(response, "Brzechwa")
        self.assertNotContains(response, "Hemar")

        hobbit = Book.objects.get(title__icontains='Hobbit')

        self.assertQuerysetEqual(response.context['books_data'], [hobbit])

    def test_list_post_with_language(self):
        url = reverse('aplikacjaKsiazkowa2:lista')
        choosen = {'p': 'pl'}
        response = self.client.post(url, choosen)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hobbit")
        self.assertContains(response, "Brzechwa")
        self.assertContains(response, "Przechrzta")
        self.assertNotContains(response, "Hemar")

        result = Book.objects.filter(language__icontains='pl')
        result_count = result.count()
        response_count = response.context['books_data'].count()

        self.assertQuerysetEqual(response.context['books_data'], result)
        self.assertEqual(result_count, response_count)

    def test_list_post_with_empty_language(self):
        url = reverse('aplikacjaKsiazkowa2:lista')
        our_lang = 'eng'
        choosen = {'language': our_lang, 'title': '', 'author': '', 'd1': '', 'd2': ''}
        response = self.client.post(url, choosen)

        self.assertEqual(response.status_code, 200)

        result = Book.objects.filter(language__icontains=our_lang)
        result_count = result.count()
        response_count = response.context['books_data'].count()

        self.assertQuerysetEqual(response.context['books_data'], result)
        self.assertEqual(result_count, response_count)

    def test_list_post_with_both_date(self):
        url = reverse('aplikacjaKsiazkowa2:lista')
        choosen = {'d1': '2001-01-01', 'd2': '2022-01-01'}
        response = self.client.post(url, choosen)

        self.assertEqual(response.status_code, 200)

    def test_list_post_with_first_date(self):
        url = reverse('aplikacjaKsiazkowa2:lista')
        choosen = {'d1': '2001-01-01'}
        response = self.client.post(url, choosen)

        self.assertEqual(response.status_code, 200)

    def test_list_post_with_second_date(self):
        url = reverse('aplikacjaKsiazkowa2:lista')
        choosen = {'d2': '2022-01-01'}
        response = self.client.post(url, choosen)

        self.assertEqual(response.status_code, 200)

    def test_list_post_with_author(self):
        url = reverse('aplikacjaKsiazkowa2:lista')
        choosen = {'q2': 'Brzechwa'}
        response = self.client.post(url, choosen)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Brzechwa")
        self.assertContains(response, "Tolkien")

        result = Book.objects.filter(author__icontains='Brzechwa')
        result_count = result.count()
        response_count = response.context['books_data'].count()

        self.assertQuerysetEqual(response.context['books_data'], result)
        self.assertEqual(result_count, response_count)


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
            'title': 'Siedem lat tłustych',
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
        self.assertEqual(response.status_code, 200)

        # self.assertRaises(ValidationError, BookCreateView.post, kwargs=book)

    def test_add_book_without_completly_only_not_null_data(self):
        book = {
            'title': 12345,
            'author': "Mikołaj Gogol Jan Kowalski Edward Nowak",
            'pub_date': '3456-12-01',
        }

        response = self.client.post(reverse('aplikacjaKsiazkowa2:add_book'), book)
        self.assertEqual(response.status_code, 302)

        books_count = Book.objects.all().count()
        self.assertEqual(1, books_count)

    def test_add_book_without_not_null_data(self):
        book = {
            'title': 'wszyscy ludzie prezydenta',
            'pub_date': "2021-02-02",
            'pages': 1234,
            'language': 'pl'
        }

        response = self.client.post(reverse('aplikacjaKsiazkowa2:add_book'), book)
        self.assertEqual(response.status_code, 302)


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

    def test_update_book_with_bad_id(self):
        url = reverse('aplikacjaKsiazkowa2:edit_book', kwargs={'pk': 100})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_update_book_with_good_id_and_data(self):
        url = reverse('aplikacjaKsiazkowa2:edit_book', kwargs={'pk': 1})
        pages = 136
        book = {
            'title': "Brzechwa misiom i innym",
            'author': "Jan Brzechwa",
            'pub_date': "2011-01-01",
            'isbn': "53387501243KS",
            'pages': pages,
            'cover': "https://bigimg.taniaksiazka.pl/images/popups/607/53387501243KS.jpg",
            'language': "PL"
        }

        response = self.client.post(url, book)

        self.assertEqual(response.status_code, 302)
        self.assertIs(Book.objects.filter(title=book['title']).exists(), True)

    def test_update_book_without_change_data(self):
        url = reverse('aplikacjaKsiazkowa2:edit_book', kwargs={'pk': 1})
        book = {
            'title': "Brzechwa dzieciom",
            'author': "Jan Brzechwa",
            'pub_date': "2011-01-01",
            'isbn': "53387501243KS",
            'pages': 136,
            'cover': "https://bigimg.taniaksiazka.pl/images/popups/607/53387501243KS.jpg",
            'language': "PL"
        }
        response = self.client.post(url, book)
        title = "Brzechwa dzieciom"

        self.assertEqual(response.status_code, 302)
        self.assertIs(Book.objects.filter(title=title).exists(), True)

    def test_update_book_without_post_data(self):
        url = reverse('aplikacjaKsiazkowa2:edit_book', kwargs={'pk': 1})
        response = self.client.post(url)
        title = "Brzechwa dzieciom"

        self.assertEqual(response.status_code, 302)
        self.assertIs(Book.objects.filter(title=title).exists(), True)


def mock_good_gugle_api() -> dict:
    book = {
        'title': "Brzechwa dzieciom",
        'author': "Jan Brzechwa",
        'pub_date': "2011-01-01",
        'isbn': "53387501243KS",
        'pages': 136,
        'cover': "https://bigimg.taniaksiazka.pl/images/popups/607/53387501243KS.jpg",
        'language': "PL"
    }
    return book


def mock_bad_gugle_api() -> dict:
    book = {
        'title': "Tuwim starym",
        'author': 213,
        'pub_date': "01-01-2345",
        'isbn': "53387501243KS",
        'pages': '136',
        'cover': "https://bigimg.taniaksiazka.pl/images/popups/607/53387501243KS.jpg",
        'language': "PL"
    }
    return book


class GugleApiViewTests(TestCase):
    def test_gugle_response(self):
        url = reverse('aplikacjaKsiazkowa2:gugle')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_gugle_api_post(self):
        book_from_api = 'Hobbit'
        url = reverse('aplikacjaKsiazkowa2:gugle')
        context = {'book_from_api': book_from_api}
        response = self.client.post(url, context)

        self.assertEqual(response.status_code, 302)


class GugleApiViewTestOnlyWithRealUsingGugleApi(TestCase):
    def test_gugle_api_with_only_test_with_real_google(self):
        book_from_api = 'Hobbit'
        url = reverse('aplikacjaKsiazkowa2:gugle')
        context = {'book_from_api': book_from_api}
        response = self.client.post(url, context)

        self.assertEqual(response.status_code, 302)

        books = Book.objects.all()
        books_count = books.count()

        self.assertNotEqual(books_count, 0)
        self.assertEqual(books_count, 10)

        if_book_exist = Book.objects.filter(title=book_from_api).exists()

        self.assertIs(if_book_exist, True)
