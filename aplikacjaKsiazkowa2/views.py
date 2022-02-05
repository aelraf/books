# -*- coding: utf-8 -*-
import requests
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Q
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
            else:
                messages.success(request, "Dodano książkę: {}".format(new_book))
        except ValidationError:
            messages.error(request, "Błąd dodawania książki: {}".format(ValidationError))
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
        messages.success(request, "Usunięto książkę: {}".format(book))
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
        pk = kwargs['pk']
        book = Book.objects.get(pk=pk)
        try:
            if 'title' in request.POST:
                book.title = request.POST.get('title')
            if 'author' in request.POST:
                book.author = request.POST.get('author')
            if 'pub_date' in request.POST:
                book.pub_date = request.POST.get('pub_date')
            if 'isbn' in request.POST:
                book.isbn = request.POST.get('isbn')
            if 'pages' in request.POST:
                book.pages = request.POST.get('pages')
            if 'cover' in request.POST:
                book.cover = request.POST.get('cover')
            if 'language' in request.POST:
                book.language = request.POST.get('language')
        except ValidationError:
            messages.error(request, "Błąd aktualizacji ksiażki - podaj poprawne dane! {}".format(ValidationError))
            return redirect('aplikacjaKsiazkowa2:edit_book')
        else:
            try:
                book.save()
                messages.success(request, "Zaktualizowano książkę: {}".format(book))
            except IntegrityError:
                messages.error(request, "Błąd aktualizacji ksiażki - IntegrityError")
                return redirect('aplikacjaKsiazkowa2:edit_book')
            else:
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

    def post(self, request):
        q = request.POST.get('q') if request.POST.get('q') is not None else ''
        q2 = request.POST.get('q2') if request.POST.get('q2') is not None else ''
        p = request.POST.get('p') if request.POST.get('p') is not None else ''
        books_data = Book.objects.filter(
            Q(title__icontains=q) |
            Q(author__icontains=q2) |
            Q(language__icontains=p)
        )

        context = {'books_data': books_data}
        print('\n lista - POST - koniec \n')
        return render(self.request, 'aplikacjaKsiazkowa2/lista.html', context)


class GugleApiView(generic.View):
    model = Book
    context_object_name = 'books_data'
    template_name = 'aplikacjaKsiazkowa2/gugleApi.html'

    def get_value_from_gugle_response(self, tab, string: str):
        value = None
        if tab.get(string) is not None:
            if string == 'imageLinks':
                value = tab[string]['thumbnail']
            else:
                value = tab[string]
        return value

    def get(self, request):
        return render(request, 'aplikacjaKsiazkowa2/gugleApi.html')

    def post(self, request):
        if 'book_from_api' in request.POST:
            book_from_gugle = request.POST.get('book_from_api')
            url_looking = 'https://www.googleapis.com/books/v1/volumes?q=' + book_from_gugle

            try:
                response = requests.get(url_looking)
                if response.status_code == 200:
                    books_data = response.json()
                    for book in books_data['items']:
                        volume = book['volumeInfo']
                        title = volume['title']

                        if volume.get('authors') is not None:
                            author = volume['authors'][0]
                        else:
                            author = "Autorzy nieznani"

                        if volume.get('publishedDate') is not None:
                            pub_date = volume['publishedDate']
                            if 4 <= len(pub_date) < 6:
                                pub_date += "-01-01"
                            elif 6 <= len(pub_date) < 8:
                                pub_date += "-01"
                        else:
                            pub_date = None

                        isbn = None
                        if volume.get('industryIdentifiers') is not None:
                            helper = volume['industryIdentifiers']
                            for i in range(len(helper)):
                                if helper[i]['type'] == 'ISBN_13':
                                    isbn = helper[i]['identifier']
                                    break

                        pages = self.get_value_from_gugle_response(volume, 'pageCount')
                        language = self.get_value_from_gugle_response(volume, 'language')
                        cover = self.get_value_from_gugle_response(volume, 'imageLinks')

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

                        messages.success(request, "Dodano książkę: {}".format(new_book))
                else:
                    messages.error(request, "błąd zapytania do gugli: ".format(response.status_code))
                    return redirect('aplikacjaKsiazkowa2:gugle')
            except IntegrityError:
                messages.error(request, "Błąd korzystania z gugleAPI - spróbuj ponownie")
                return redirect('aplikacjaKsiazkowa2:gugle')
            else:
                print('\n')
                return redirect('aplikacjaKsiazkowa2:lista')


"""
class BookViewSet(viewsets.ModelViewSet):
    # początek widoku ogólnego REST API za widok my_api 
    queryset = Book.objects.all()
    serializer_class = BookSerializer
"""
