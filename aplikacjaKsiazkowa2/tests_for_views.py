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


class BookUpdateViewTest(TestCase):
    def test_update_book(self):
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
        # wynik = Book.objects.filter(title="Brzechwa misiom i innym").exists()
        # print("test_edit_book_post: {}".format(wynik))
        # self.assertIs(wynik, True)
