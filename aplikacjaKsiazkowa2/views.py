# -*- coding: utf-8 -*-
import datetime

from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages

from aplikacjaKsiazkowa2.models import Book

from rest_framework import viewsets
from .serializer import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


def index(request):
    messages.success(request, "Dzień dobry!")
    return render(request, 'aplikacjaKsiazkowa2/index.html')


def edit(request, id):
    edytowana = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        messages.success(request, "POST - Edytujesz książkę o id: {}".format(id))
        title = request.POST.get('title')
        author = request.POST.get('author')
        data = request.POST.get('pub_date')
        isbn = request.POST.get('isbn')
        pages = request.POST.get('pages')
        cover = request.POST.get('cover')
        languague = request.POST.get('languague')

        if edytowana.title != title:
            edytowana.title = title
        if edytowana.author != author:
            edytowana.author = author
        if edytowana.pub_date != data:
            edytowana.pub_date = data
        if edytowana.isbn != isbn:
            edytowana.isbn = isbn
        if edytowana.pages != pages:
            edytowana.pages = pages
        if edytowana.cover != cover:
            edytowana.cover = cover
        if edytowana.languague != languague:
            edytowana.languague = languague
        edytowana.save()

        data = Book.objects.order_by('id')
        context = {"books_data": data}
        return render(request, 'aplikacjaKsiazkowa2/lista.html', context)

    context = {'book': edytowana}
    return render(request, 'aplikacjaKsiazkowa2/edit.html', context)


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
        lang = request.POST.get('languague')
        print("tytul= {}, {}, {}, {}, {}, {}, {}".format(tytul, autor, pub_date, isbn, pages, cover, lang))
        try:
            nowa = Book(
                title=tytul,
                author=autor,
                pub_date=pub_date,
                isbn=isbn,
                pages=pages,
                cover=cover,
                languague=lang
            )
            nowa.save()
        except ValueError:
            print("ValueError")
            messages.error(request, "ValueError.")
        except ValidationError:
            messages.error(request, "ValidationError")
        else:
            messages.success(request, "Dodano nową książkę - POST: {}".format(tytul))

        return render(request, 'aplikacjaKsiazkowa2/add_book.html')

    messages.success(request, "Dodawanie książki - GET.")
    print("add_book - GET")
    print(datetime.datetime.now())
    return render(request, 'aplikacjaKsiazkowa2/add_book.html')


def lista(request):
    if request.method == "POST":
        data = Book.objects.order_by('id')
        d1 = datetime.date.today()
        d2 = datetime.date.today()
        jezyk = "PL"
        tytul = "Tytuł"
        autor = "Autor"
        try:
            d1 = request.POST.get('d1')
            d2 = request.POST.get('d2')
            jezyk = request.POST.get('languague')
            tytul = request.POST.get('title')
            autor = request.POST.get('author')
        except TypeError:
            messages.error("Type error - brak wartości wyszukiwania")
        else:
            if len(d1) and len(d2):
                print("Lista - wyszukiwanie po przedziale daty: ")
                print('\n lista - metoda POST, d1= {}, d2= {}'.format(d1, d2))
                try:
                    data = Book.objects.filter(pub_date__range=(d1, d2))
                except ValidationError:
                    messages.warning(request, "ValidationError - zła data! Podaj prawidłowy zakres!")
                else:
                    if not data.exists():
                        messages.warning(request, "Pusty zakres przeszukiwania dat!")

            if len(jezyk):
                print('Lista - Wyszukiwanie po języku: {} \n'.format(jezyk))
                try:
                    data = Book.objects.filter(languague__contains=jezyk)
                except ValidationError:
                    messages.warning(request, "ValidationError - zły język! Podaj prawidłowe dane!")
                else:
                    if not data.exists():
                        messages.warning(request, "Brak książek tego języka")

            if len(tytul):
                print('Lista - wyszukiwanie po tytule: {} \n'.format(tytul))
                try:
                    data = Book.objects.filter(title__contains=tytul)
                except ValidationError:
                    messages.warning(request, "ValidationError - zły tytuł! Podaj prawidłowe dane!")
                else:
                    if not data.exists():
                        messages.warning(request, "Brak książek o tym tytule")

            if len(autor):
                print("lista - wyszukiwanie po autorze: {} \n ".format(autor))
                try:
                    data = Book.objects.filter(author__contains=autor)
                except ValidationError:
                    messages.warning(request, "ValidationError - zły autor! Podaj prawidłowe dane!")
                else:
                    if not data.exists():
                        messages.warning(request, "Brak książek tego autora")

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
    return render(request, 'aplikacjaKsiazkowa2/gugleApi.html')