# -*- coding: utf-8 -*-
import datetime

import requests
# from django.core import serializers
from django.core.exceptions import ValidationError
# from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.utils.dateparse import parse_date
# from django.utils.datetime_safe import date
from django.views import generic, View
from django.views.generic import UpdateView

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status

from aplikacjaKsiazkowa2.models import Book
# from . import serializer
from .serializer import BookSerializer


class IndexView(generic.ListView):
    """ widok generyczny w zamian za widok index(request) """
    template_name = 'aplikacjaKsiazkowa2/index.html'


def index(request):
    # messages.success(request, "Dzień dobry!")
    return render(request, 'aplikacjaKsiazkowa2/index.html')


class BookViewSet(viewsets.ModelViewSet):
    """ początek widoku generycznego REST API za widok my_api """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


@api_view(['GET', 'POST'])
def my_api(request):
    """
    Widok REST API posiadający listę książek z wyszukiwaniem i filtrowaniem przy użyciu query string,
    po tytule, autorze, języku oraz zakresie dat.

    Parametry:
    title - tytuł
    author - autor
    language - język
    start_date - data początkowa (format: YYYY-MM-DD)
    end_date - data końcowa (format: YYYY-MM-DD)
    """
    if 'author' in request.GET:
        print("my_api - autor: ")
        author = request.GET['author']
        try:
            data = Book.objects.filter(author__contains=author)
            serial = BookSerializer(data, many=True)
            return Response(serial.data)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif 'title' in request.GET:
        print("my_api - tytuł")
        title = request.GET['title']
        try:
            data = Book.objects.filter(title__contains=title)
            serial = BookSerializer(data, many=True)
            return Response(serial.data)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif 'language' in request.GET:
        print("my_api - język")
        language = request.GET['language']
        try:
            data = Book.objects.filter(language__contains=language)
            serial = BookSerializer(data, many=True)
            return Response(serial.data)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif 'start_date' in request.GET and 'end_date' in request.GET:
        print("my_api - zakres dat")
        try:
            start_date = parse_date(request.GET['start_date'])
            end_date = parse_date(request.GET['end_date'])

            data = Book.objects.filter(pub_date__range=(start_date, end_date))
            serial = BookSerializer(data, many=True)
            return Response(serial.data)
        except ValidationError:
            messages.error(request, "Błąd validacji - zły format daty")
            print("my_api - bad request dla dat.")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    else:
        print("metoda my_api: {}".format(request))
        try:
            data = Book.objects.order_by('id')
            serial = BookSerializer(data, many=True)
            return Response(serial.data)
        except AttributeError:
            messages.error(request, "Błąd - Attribute error w metodzie my_api")
            print("Blad - Attribute error w metodzie my_api")
            return Response(status=status.HTTP_400_BAD_REQUEST)


class BookUpdateView(UpdateView):
    """ drugi widok klasowy w zamian za metodę edit() """
    model = Book
    fields = '__all__'
    template_name = 'aplikacjaKsiazkowa2/edit.html'
    context_object_name = 'books_data'
    success_url = 'aplikacjaKsiazkowa2/lista.html'


def add_book(request):
    if request.method == 'POST':
        print("add_book - POST")
        print(datetime.datetime.now())

        tytul = request.POST.get('title')
        autor = request.POST.get('author')
        pub_date = request.POST.get('pub_date')
        isbn = request.POST.get('isbn')
        pages = request.POST.get('pages')
        cover = request.POST.get('cover')
        lang = request.POST.get('language')
        # print("tytul= {}, {}, {}, {}, {}, {}, {}".format(tytul, autor, pub_date, isbn, pages, cover, lang))
        try:
            nowa = Book(
                title=tytul,
                author=autor,
                pub_date=pub_date,
                isbn=isbn,
                pages=pages,
                cover=cover,
                language=lang
            )
            nowa.save()
        except ValueError:
            print("ValueError")
            messages.error(request, "ValueError.")
        except ValidationError:
            messages.error(request, "ValidationError - błąd typu danych")
        else:
            messages.success(request, "Dodano nową książkę - POST: {}".format(tytul))

        return render(request, 'aplikacjaKsiazkowa2/add_book.html')

    # messages.success(request, "Dodawanie książki - GET.")
    print("add_book - GET")
    print(datetime.datetime.now())
    return render(request, 'aplikacjaKsiazkowa2/add_book.html')


class ListBookView(generic.ListView):
    template_name = 'aplikacjaKsiazkowa2/lista.html'
    context_object_name = 'books_data'

    def get_queryset(self):
        data = Book.objects.order_by('id')
        context = {"books_data": data}
        return render(self.request, 'aplikacjaKsiazkowa2/lista.html', context)

    def post(self):
        if self.request.method == "POST":
            data = Book.objects.order_by('id')

            if 'd1' in self.request.POST and 'd2' in self.request.POST:
                d1 = self.request.POST.get('d1')
                d2 = self.request.POST.get('d2')
                print("Lista - wyszukiwanie po przedziale daty: ")
                print('\n lista - metoda POST, d1= {}, d2= {}'.format(d1, d2))
                try:
                    data = Book.objects.filter(pub_date__range=(d1, d2))
                except ValidationError:
                    messages.warning(self.request, "ValidationError - zła data! Podaj prawidłowy zakres!")
                else:
                    if not data.exists():
                        messages.warning(self.request, "Pusty zakres przeszukiwania dat!")
                    context = {'books_data': data}
                    return render(self.request, 'aplikacjaKsiazkowa2/lista.html', context)

            if 'language' in self.request.POST:
                jezyk = self.request.POST.get('language')
                print('Lista - Wyszukiwanie po języku: {}  \n'.format(jezyk))
                try:
                    data = Book.objects.filter(language__contains=jezyk)
                except ValidationError:
                    messages.warning(self.request, "ValidationError - zły język! Podaj prawidłowe dane!")
                else:
                    if not data.exists():
                        messages.warning(self.request, "Brak książek tego języka")
                    context = {'books_data': data}
                    return render(self.request, 'aplikacjaKsiazkowa2/lista.html', context)

            if 'title' in self.request.POST:
                tytul = self.request.POST.get('title')
                print('Lista - wyszukiwanie po tytule: {} \n'.format(tytul))
                try:
                    data = Book.objects.filter(title__contains=tytul)
                except ValidationError:
                    messages.warning(self.request, "ValidationError - zły tytuł! Podaj prawidłowe dane!")
                else:
                    if not data.exists():
                        messages.warning(self.request, "Brak książek o tym tytule")
                    context = {'books_data': data}
                    return render(self.request, 'aplikacjaKsiazkowa2/lista.html', context)

            if 'author' in self.request.POST:
                autor = self.request.POST.get('author')
                print("lista - wyszukiwanie po autorze: {} \n ".format(autor))
                try:
                    data = Book.objects.filter(author__contains=autor)
                except ValidationError:
                    messages.warning(self.request, "ValidationError - zły autor! Podaj prawidłowe dane!")
                else:
                    if not data.exists():
                        messages.warning(self.request, "Brak książek tego autora")
                    context = {'books_data': data}
                    return render(self.request, 'aplikacjaKsiazkowa2/lista.html', context)

            context = {'books_data': data}
            print('\n lista - POST - koniec \n')
            return render(self.request, 'aplikacjaKsiazkowa2/lista.html', context)


def lista(request):
    if request.method == "POST":
        data = Book.objects.order_by('id')

        if 'd1' in request.POST and 'd2' in request.POST:
            d1 = request.POST.get('d1')
            d2 = request.POST.get('d2')
            print("Lista - wyszukiwanie po przedziale daty: ")
            print('\n lista - metoda POST, d1= {}, d2= {}'.format(d1, d2))
            try:
                data = Book.objects.filter(pub_date__range=(d1, d2))
            except ValidationError:
                messages.warning(request, "ValidationError - zła data! Podaj prawidłowy zakres!")
            else:
                if not data.exists():
                    messages.warning(request, "Pusty zakres przeszukiwania dat!")
                context = {'books_data': data}
                return render(request, 'aplikacjaKsiazkowa2/lista.html', context)

        if 'language' in request.POST:
            jezyk = request.POST.get('language')
            print('Lista - Wyszukiwanie po języku: {}  \n'.format(jezyk))
            try:
                data = Book.objects.filter(language__contains=jezyk)
            except ValidationError:
                messages.warning(request, "ValidationError - zły język! Podaj prawidłowe dane!")
            else:
                if not data.exists():
                    messages.warning(request, "Brak książek tego języka")
                context = {'books_data': data}
                return render(request, 'aplikacjaKsiazkowa2/lista.html', context)

        if 'title' in request.POST:
            tytul = request.POST.get('title')
            print('Lista - wyszukiwanie po tytule: {} \n'.format(tytul))
            try:
                data = Book.objects.filter(title__contains=tytul)
            except ValidationError:
                messages.warning(request, "ValidationError - zły tytuł! Podaj prawidłowe dane!")
            else:
                if not data.exists():
                    messages.warning(request, "Brak książek o tym tytule")
                context = {'books_data': data}
                return render(request, 'aplikacjaKsiazkowa2/lista.html', context)

        if 'author' in request.POST:
            autor = request.POST.get('author')
            print("lista - wyszukiwanie po autorze: {} \n ".format(autor))
            try:
                data = Book.objects.filter(author__contains=autor)
            except ValidationError:
                messages.warning(request, "ValidationError - zły autor! Podaj prawidłowe dane!")
            else:
                if not data.exists():
                    messages.warning(request, "Brak książek tego autora")
                context = {'books_data': data}
                return render(request, 'aplikacjaKsiazkowa2/lista.html', context)

        context = {'books_data': data}
        print('\n lista - POST - koniec \n')
        return render(request, 'aplikacjaKsiazkowa2/lista.html', context)

    data = Book.objects.order_by('id')
    context = {"books_data": data}
    return render(request, 'aplikacjaKsiazkowa2/lista.html', context)


def delete(request, id):
    print("*************** metoda delete **************** ")
    print("id ksiazki usuwanej: {}".format(id))
    print("metoda: {}".format(request.method))
    usuwany = get_object_or_404(Book, id=id)
    if request.method == "GET":
        print("delete - GET: {}".format(usuwany))
        usuwany.delete()
    if request.method == "POST":
        print("delete - POST")
        usuwany.delete()
    if request.method == "DELETE":
        print("Delete - DELETE")

    messages.warning(request, "Usuwasz książkę o id={}".format(id))
    data = Book.objects.order_by('id')
    context = {"books_data": data}
    return render(request, 'aplikacjaKsiazkowa2/lista.html', context)


def gugle(request):
    if request.method == "POST":
        if 'terms' in request.POST:
            terms = request.POST.get('terms')
            url_looking = 'https://www.googleapis.com/books/v1/volumes?q=' + terms
            response = requests.get(url_looking)
            if response.status_code == 200:
                print("Status code == 200")
                books_data = response.json()
                for book in books_data['items']:
                    volume = book['volumeInfo']
                    title = volume['title']

                    if volume.get('authors') is not None:
                        author = volume['authors'][0]
                    else:
                        author = "Autorzy nieznani"

                    pub_date = volume['publishedDate']
                    if 4 <= len(pub_date) < 6:
                        pub_date += "-01-01"
                    elif 6 <= len(pub_date) < 8:
                        pub_date += "-01"

                    i = volume['industryIdentifiers']
                    isbn = 0
                    for j in range(len(i)):
                        if i[j]['type'] == 'ISBN_13':
                            print("\n isbn: {}, {}".format(i[j]['type'], i[j]['identifier']))
                            isbn = i[j]['identifier']
                            break
                        else:
                            isbn = None

                    if volume.get("pageCount") is not None:
                        pages = volume.get("pageCount")
                    else:
                        pages = None

                    if volume.get('imageLinks') is not None:
                        # print("okładka: {}".format(volume['imageLinks']))
                        cover = volume.get('imageLinks')['thumbnail']
                        # print("cover: {}".format(cover))
                    else:
                        cover = None
                    if volume.get('language') is not None:
                        language = volume['language']
                        # print('language: {}'.format(language))
                    else:
                        language = None
                    print("book: {}, {}, {}, {}, {}, {}, {} "
                          .format(title, author, pub_date, isbn, pages, cover, language))

                    new_book = Book(
                        title=title,
                        author=author,
                        pub_date=pub_date,
                        isbn=isbn,
                        pages=pages,
                        cover=cover,
                        language=language
                    )
                    new_book.save()

            messages.success(request, "Książki dodano do listy.")
            return render(request, 'aplikacjaKsiazkowa2/index.html')

        else:
            messages.warning(request, "złe zapytanie!")
            return Response(status=status.HTTP_400_BAD_REQUEST)

    else:
        return render(request, 'aplikacjaKsiazkowa2/gugleApi.html')
