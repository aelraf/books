# -*- coding: utf-8 -*-
import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from aplikacjaKsiazkowa2.models import Book


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
        languague=book.languague
    )


class BookViewTests(TestCase):
    def test_no_book(self):
        response = self.client.get(reverse('aplikacjaKsiazkowa2:lista'))
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(response.context['books_data'], [])

    def test_list_book(self):
        response = self.client.get(reverse('aplikacjaKsiazkowa2:lista'))
        self.assertEqual(response.status_code, 200)
        books_data = Book.objects.order_by('id')

        self.assertQuerysetEqual(response.context['books_data'], books_data)

    def test_list_book_date_between_d1_and_d2(self):
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

    def test_list_book_select_languague(self):
        jezyk = "ENG"
        response = self.client.post(reverse('aplikacjaKsiazkowa2:lista'), {'jezyk': jezyk})
        code = response.status_code
        self.assertEqual(code, 200)
        print("kod odpowiedzi: {}".format(code))
        books_data = Book.objects.filter(languague__contains=jezyk)

        self.assertQuerysetEqual(response.context['books_data'], books_data)

    def test_list_book_select_title(self):
        tytul = "Hobbit"
        response = self.client.post(reverse('aplikacjaKsiazkowa2:lista'), {'tytul': tytul})
        code = response.status_code
        self.assertEqual(code, 200)
        print("kod odpowiedzi: {}".format(code))
        books_data = Book.objects.filter(title__contains=tytul)

        self.assertQuerysetEqual(response.context['books_data'], books_data)

    def test_list_book_select_author(self):
        autor = "Jan"
        response = self.client.post(reverse('aplikacjaKsiazkowa2:lista'), {'autor': autor})
        code = response.status_code
        self.assertEqual(code, 200)
        print("kod odpowiedzi: {}".format(code))
        books_data = Book.objects.filter(title__contains=autor)

        self.assertQuerysetEqual(response.context['books_data'], books_data)

    def test_add_book_get(self):
        response = self.client.get(reverse('aplikacjaKsiazkowa2:add_book'))
        self.assertEqual(response.status_code, 200)

    def test_add_book_add_good_book(self):
        book = Book(
            title="Brzechwa dzieciom",
            author="Jan Brzechwa",
            pub_date="2011-01-01",
            isbn="53387501243KS",
            pages=136,
            cover="https://bigimg.taniaksiazka.pl/images/popups/607/53387501243KS.jpg",
            languague="PL"
        )
        create_book(book)

        response = self.client.post(reverse('aplikacjaKsiazkowa2:add_book'),
                                    {'title': book.title,
                                     'author': book.author,
                                     'pub_date': book.pub_date,
                                     'isbn': book.isbn,
                                     'pages': book.pages,
                                     'cover': book.cover,
                                     'languague': book.languague
                                     })
        self.assertEqual(response.status_code, 200)





