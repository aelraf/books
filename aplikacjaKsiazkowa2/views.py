# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
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


class BookCreateView(CreateView):
    # widok klasowy za metodę add_book
    model = Book
    fields = '__all__'
    template_name = 'aplikacjaKsiazkowa2/add_book.html'
    context_object_name = 'books_data'

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        new_book, created = Book.objects.get_or_create(
            title=title,
            author=request.POST.get('author'),
            pub_date=request.POST.get('pub_date'),
            isbn=request.POST.get('isbn'),
            pages=request.POST.get('pages'),
            cover=request.POST.get('cover'),
            language=request.POST.get('language')
        )
        if created is False:
            messages.error("Błąd dodawania książki")
            return render(request, 'aplikacjaKsiazkowa2/add_book.html')

        print("BookCreateView: post: new_book: {}, created: {} ".format(new_book, created))

        # return render(request, 'aplikacjaKsiazkowa2/add_book.html')
        return redirect('aplikacjaKsiazkowa2:lista')


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'aplikacjaKsiazkowa2/delete.html'
    success_url = 'aplikacjaKsiazkowa2/lista.html'

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        book = Book.objects.get(id=pk)
        print('BookDeleteView - usuwamy książkę o id: {}'.format(pk))
        book.delete()
        return redirect('aplikacjaKsiazkowa2:lista')


"""
class BookViewSet(viewsets.ModelViewSet):
    # początek widoku ogólnego REST API za widok my_api 
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookUpdateView(UpdateView):
    # drugi widok klasowy w zamian za metodę edit() 
    model = Book
    fields = '__all__'
    template_name = 'aplikacjaKsiazkowa2/edit.html'
    context_object_name = 'books_data'
    success_url = 'aplikacjaKsiazkowa2/lista.html'

"""


class ListBookView(generic.ListView):
    model = Book
    context_object_name = 'books_data'
    template_name = 'aplikacjaKsiazkowa2/lista.html'
    queryset = Book.objects.all()
    # https://getbootstrap.com/docs/5.1/content/tables/
    # https://www.dennisivy.com/post/django-class-based-views/

    # def get_queryset(self):
    #    books_data = Book.objects.all()
    #    context = {'books_data': books_data}
    #    return render(self.request, 'aplikacjaKsiazkowa2/lista.html', context)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books_data'] = Book.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = Book.objects.order_by('id')

        q = request.POST.get('q') if request.POST.get('q') is not None else ''

        context = {'books_data': data }
        print('\n lista - POST - koniec \n')
        return render(self.request, 'aplikacjaKsiazkowa2/lista.html', context)









