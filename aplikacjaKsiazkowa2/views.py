# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages

from django.views import generic
from django.views.generic import UpdateView, CreateView, DeleteView

from rest_framework import viewsets

from aplikacjaKsiazkowa2.models import Book
from .forms import BookForm
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
        try:
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
                messages.error(request, "Błąd dodawania książki")
                return render(request, 'aplikacjaKsiazkowa2/add_book.html')
        except ValidationError:
            messages.error(request, "Błąd dodawania książki")
            return render(request, 'aplikacjaKsiazkowa2/add_book.html')
        else:
            return redirect('aplikacjaKsiazkowa2:lista')


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'aplikacjaKsiazkowa2/delete.html'
    success_url = 'aplikacjaKsiazkowa2/lista.html'

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        book = Book.objects.get(id=pk)
        book.delete()
        return redirect('aplikacjaKsiazkowa2:lista')


class BookUpdateView(UpdateView):
    # drugi widok klasowy w zamian za metodę edit()
    model = Book
    fields = '__all__'
    template_name = 'aplikacjaKsiazkowa2/edit.html'
    # context_object_name = 'books_data'
    success_url = 'aplikacjaKsiazkowa2/lista.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        try:
            book = Book.objects.get(pk=pk)
        except KeyError:
            messages.error(request, "Błąd aktualizacji ksiażki - KeyError!")
            return redirect('aplikacjaKsiazkowa2:lista')
        except:
            messages.error(request, "Błąd aktualizacji ksiażki - książki o takim id nie ma w bazie!")
            return redirect('aplikacjaKsiazkowa2:lista')
        else:
            form = BookForm(instance=book)
            context = {'form': form, 'book': book}

            return render(request, 'aplikacjaKsiazkowa2/edit.html', context)

    def post(self, request, *args, **kwargs):
        print('UpdateBook: 1')
        pk = kwargs['pk']
        book = Book.objects.get(pk=pk)
        print('UpdateBook: 2')
        try:
            print('UpdateBook: 3')
            book.title = request.POST.get('title')
            book.author = request.POST.get('author')
            book.pub_date = request.POST.get('pub_date')
            book.isbn = request.POST.get('isbn')
            book.pages = request.POST.get('pages')
            book.cover = request.POST.get('cover')
            book.language = request.POST.get('language')
            print('UpdateBook: 4')
        except ValidationError:
            print('UpdateBook: 5 - ValidationError')
            messages.error(request, "Błąd aktualizacji ksiażki - podaj poprawne dane!")
            return redirect('aplikacjaKsiazkowa2:edit_book')
        else:
            print('UpdateBook: 6')
            try:
                book.save()
                print('UpdateBook: 7')
            except IntegrityError:
                print('UpdateBook: 8 - IntegrityError')
                messages.error(request, "Błąd aktualizacji ksiażki - IntegrityError")
                return redirect('aplikacjaKsiazkowa2:edit_book')
            else:
                print('UpdateBook: 9 \n\n')
                return redirect('aplikacjaKsiazkowa2:lista')


class ListBookView(generic.ListView):
    model = Book
    context_object_name = 'books_data'
    template_name = 'aplikacjaKsiazkowa2/lista.html'
    queryset = Book.objects.all()

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


"""
class BookViewSet(viewsets.ModelViewSet):
    # początek widoku ogólnego REST API za widok my_api 
    queryset = Book.objects.all()
    serializer_class = BookSerializer
"""
