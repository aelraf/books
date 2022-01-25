# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.contrib import messages

from django.views import generic
from django.views.generic import UpdateView, CreateView, DeleteView

from rest_framework import viewsets

from aplikacjaKsiazkowa2.models import Book
from .serializer import BookSerializer


class IndexView(generic.ListView):
    """ widok ogólny w zamian za widok index(request) """
    template_name = 'aplikacjaKsiazkowa2/index.html'
    queryset = Book.objects.all()
    context_object_name = 'books_data'


class BookViewSet(viewsets.ModelViewSet):
    """ początek widoku ogólnego REST API za widok my_api """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookCreateView(CreateView):
    """ widok klasowy za metodę add_book"""
    model = Book
    fields = '__all__'
    template_name = 'aplikacjaKsiazkowa2/add_book.html'
    context_object_name = 'books_data'


class BookUpdateView(UpdateView):
    """ drugi widok klasowy w zamian za metodę edit() """
    model = Book
    fields = '__all__'
    template_name = 'aplikacjaKsiazkowa2/edit.html'
    context_object_name = 'books_data'
    success_url = 'aplikacjaKsiazkowa2/lista.html'


class BookDeleteView(DeleteView):
    model = Book
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









