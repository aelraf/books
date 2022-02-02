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

    def post(self, request, *args, **kwargs):
        data = Book.objects.order_by('id')

        q = request.POST.get('q') if request.POST.get('q') is not None else ''

        context = {'books_data': data}
        print('\n lista - POST - koniec \n')
        return render(self.request, 'aplikacjaKsiazkowa2/lista.html', context)









