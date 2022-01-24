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


class BookViewSet(viewsets.ModelViewSet):
    """ początek widoku generycznego REST API za widok my_api """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookUpdateView(UpdateView):
    """ drugi widok klasowy w zamian za metodę edit() """
    model = Book
    fields = '__all__'
    template_name = 'aplikacjaKsiazkowa2/edit.html'
    context_object_name = 'books_data'
    success_url = 'aplikacjaKsiazkowa2/lista.html'


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









