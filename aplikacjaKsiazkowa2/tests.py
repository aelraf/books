# -*- coding: utf-8 -*-
import datetime

import requests
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIRequestFactory, RequestsClient

from aplikacjaKsiazkowa2.models import Book
from aplikacjaKsiazkowa2.views import my_api


class BookModelClass(TestCase):
    def test_was_published_recently(self):
        time = timezone.now() + datetime.timedelta(days=5)
        future_book = Book(pub_date=time)

        self.assertIs(future_book.was_published_recently(), False)

    def test_was_published_recently_old(self):
        time = timezone.now() + datetime.timedelta(days=1, seconds=1)
        old_book = Book(pub_date=time)

        self.assertIs(old_book.was_published_recently(), False)


def create_book(book):
    return Book.objects.create(
        title=book.title,
        author=book.author,
        pub_date=book.pub_date,
        isbn=book.isbn,
        pages=book.pages,
        cover=book.cover,
        language=book.language
    )


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


class BookViewTests(TestCase):
    def test_index(self):
        response = self.client.get(reverse('aplikacjaKsiazkowa2:index'))
        self.assertEqual(response.status_code, 200)

    def test_no_book(self):
        response = self.client.get(reverse('aplikacjaKsiazkowa2:lista'))
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(response.context['books_data'], [])

    def test_list_book(self):
        create_brzechwa()
        response = self.client.get(reverse('aplikacjaKsiazkowa2:lista'))
        self.assertEqual(response.status_code, 200)
        books_data = Book.objects.order_by('id')

        self.assertQuerysetEqual(response.context['books_data'], books_data)

    def test_list_book_date_between_d1_and_d2(self):
        create_brzechwa()
        d_p = datetime.date(1999, 1, 1)
        d_k = datetime.date.today()
        response = self.client.post(reverse('aplikacjaKsiazkowa2:lista'), {
            'd1': datetime.date(1999, 1, 1),
            'd2': datetime.date.today()})
        code = response.status_code
        self.assertEqual(code, 200)
        print("kod odpowiedzi: {}".format(code))
        books_data = Book.objects.filter(pub_date__range=(d_p, d_k))

        self.assertQuerysetEqual(response.context['books_data'], books_data)

    def test_list_book_select_language(self):
        create_brzechwa()
        jezyk = "pl"
        response = self.client.post(reverse('aplikacjaKsiazkowa2:lista'), {'jezyk': jezyk})
        code = response.status_code
        self.assertEqual(code, 200)
        print("kod odpowiedzi: {}".format(code))
        books_data = Book.objects.filter(language__contains=jezyk)

        self.assertQuerysetEqual(response.context['books_data'], books_data)

    def test_list_book_select_title(self):
        create_brzechwa()
        tytul = "Brzechwa"
        response = self.client.post(reverse('aplikacjaKsiazkowa2:lista'), {'tytul': tytul})
        code = response.status_code
        self.assertEqual(code, 200)
        print("kod odpowiedzi: {}".format(code))
        books_data = Book.objects.filter(title__contains=tytul)

        self.assertQuerysetEqual(response.context['books_data'], books_data)

    def test_list_book_select_author(self):
        create_brzechwa()
        autor = "Jan"
        response = self.client.post(reverse('aplikacjaKsiazkowa2:lista'), {'autor': autor})
        code = response.status_code
        self.assertEqual(code, 200)
        print("kod odpowiedzi: {}".format(code))
        books_data = Book.objects.filter(author__contains=autor)

        self.assertQuerysetEqual(response.context['books_data'], books_data)

    def test_add_book_get(self):
        response = self.client.get(reverse('aplikacjaKsiazkowa2:add_book'))

        self.assertEqual(response.status_code, 200)

    def test_add_book_post(self):
        book = Book(
            title="Brzechwa dzieciom",
            author="Jan Brzechwa",
            pub_date="2011-01-01",
            isbn="53387501243KS",
            pages=136,
            cover="https://bigimg.taniaksiazka.pl/images/popups/607/53387501243KS.jpg",
            language="PL"
        )
        response = self.client.post(reverse('aplikacjaKsiazkowa2:add_book'),
                                    {'title': book.title,
                                     'author': book.author,
                                     'pub_date': book.pub_date,
                                     'isbn': book.isbn,
                                     'pages': book.pages,
                                     'cover': book.cover,
                                     'language': book.language
                                     })
        self.assertEqual(response.status_code, 200)

        self.assertIs(Book.objects.filter(title=book.title).exists(), True)

    def test_edit_book_get_good_id(self):
        book = create_brzechwa()
        url = reverse('aplikacjaKsiazkowa2:edit', kwargs={'id': 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_edit_book_get_bad_id(self):
        url = reverse('aplikacjaKsiazkowa2:edit', kwargs={'id': 100})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_edit_book_post(self):
        book = create_brzechwa()
        url = reverse('aplikacjaKsiazkowa2:edit', kwargs={'id': 1})
        response = self.client.post(url, {
            'title': "Brzechwa misiom i innym",
            'author': book.author,
            'pub_date': book.pub_date,
            'isbn': book.isbn,
            'pages': book.pages,
            'cover': book.cover,
            'language': book.language
        })
        self.assertEqual(response.status_code, 200)
        wynik = Book.objects.filter(title="Brzechwa misiom i innym").exists()
        print("test_edit_book_post: {}".format(wynik))
        self.assertIs(wynik, True)

    def test_delete_book_get_good_id(self):
        book = create_brzechwa()
        url = reverse('aplikacjaKsiazkowa2:delete', kwargs={'id': 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_delete_book_get_bad_id(self):
        url = reverse('aplikacjaKsiazkowa2:delete', kwargs={'id': 100})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_delete_book_past(self):
        book = create_brzechwa()
        url = reverse('aplikacjaKsiazkowa2:delete', kwargs={'id': 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        books_data = Book.objects.all()

        self.assertQuerysetEqual(response.context['books_data'], books_data)


class RESTApiTests(TestCase):
    def test_my_api_without_params(self):
        book = create_brzechwa()
        factory = APIRequestFactory()
        url = reverse('aplikacjaKsiazkowa2:my_api')
        requests = factory.get(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_my_api_with_author(self):
        book = create_brzechwa()
        books = Book.objects.get(author__contains="Jan")

        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/my_api/?author=Jan')
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result[0]['author'], books.author)

    def test_my_api_with_title(self):
        book = create_brzechwa()
        books = Book.objects.get(title__contains="dzieciom")

        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/my_api/?title=dzieciom')
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result[0]['title'], books.title)

    def test_my_api_with_language(self):
        book = create_brzechwa()
        books = Book.objects.filter(language__contains="PL")

        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/my_api/?language=PL')
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result[0]['language'], 'PL')

    def test_my_api_with_start_and_stop_date(self):
        book = create_brzechwa()

        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/my_api/?start_date=2010-01-01&end_date=2021-01-01')
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 1)

    def test_my_api_with_only_start_date(self):
        """
        Jeśli podamy tylko jedną z dat, to zwróci nam całą listę, bo przedział musi być obustronny.
        """
        book = create_brzechwa()
        books = Book.objects.all()

        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/my_api/?start_date=2010-01-01')
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), len(books))

    def test_my_api_with_bad_date(self):
        """
        Sprawdzamy, czy dostaniemy AssertionError.
        """
        book = create_brzechwa()

        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/my_api/?start_date=2010-31-51&end_date=2021-21-41')

        self.assertEqual(response.status_code, 500)


class GugleApiTests(TestCase):
    def test_gugle_get(self):
        url = reverse('aplikacjaKsiazkowa2:gugle')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_gugle_post_and_exist(self):
        # co jest zwracane przez naszą metodę
        terms = "Hobbit"
        url = reverse('aplikacjaKsiazkowa2:gugle')
        response = self.client.post(url, {'terms': terms})
        code = response.status_code
        books_data_i = Book.objects.count()

        self.assertEqual(code, 200)

        # co jest zwracane przez APIGoogla
        url_looking = 'https://www.googleapis.com/books/v1/volumes?q=' + terms
        s = requests.Session()
        response_gugiel = s.get(url_looking)
        gugiel_i = 0
        for g in response_gugiel.json()['items']:
            gugiel_i += 1
        # print("\n count book: {}".format(books_data_i))
        # print("\n gugiel: {}".format(gugiel_i))

        self.assertEqual(response_gugiel.status_code, 200)
        # czy zbiory są równoliczne
        self.assertIs(books_data_i, gugiel_i)

    def test_gugle_post_not_exist(self):
        # terms = "Buzikawoeslaoeasdzasakcemolesowiatretabialozeneorelion"
        terms = ""
        url = reverse('aplikacjaKsiazkowa2:gugle')
        response = self.client.post(url, {'terms': terms})
        # print("\n test_gugle_post_not_exist\n")
        # print(response.context)
        code = response.status_code
        print(code)

        self.assertEqual(code, 200)


