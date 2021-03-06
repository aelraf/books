# -*- coding: utf-8 -*-
import requests
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy

from django.views import generic
from django.views.generic import UpdateView, CreateView, DeleteView
from rest_framework import status

from aplikacjaKsiazkowa2.models import Book
from .forms import BookForm


class IndexView(generic.TemplateView):
    """ widok ogólny w zamian za widok index(request) """
    template_name = 'aplikacjaKsiazkowa2/index.html'


class OurApiView(generic.TemplateView):
    template_name = "aplikacjaKsiazkowa2/naszeApi.html"


class BookCreateView(CreateView):
    model = Book
    fields = '__all__'
    template_name = 'aplikacjaKsiazkowa2/add_book.html'
    context_object_name = 'books_data'
    success_url = reverse_lazy('aplikacjaKsiazkowa2:lista')


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
    # widok odpowiedzialny za edycję książek
    model = Book
    fields = '__all__'
    template_name = 'aplikacjaKsiazkowa2/edit.html'
    success_url = 'aplikacjaKsiazkowa2/lista.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk'] if 'pk' in kwargs else ''
        try:
            book = Book.objects.get(pk=pk)
        except KeyError as err:
            messages.error(request, "Błąd aktualizacji ksiażki - KeyError! {}".format(err))
            return redirect('aplikacjaKsiazkowa2:lista')
        except:
            messages.error(request, "Błąd aktualizacji ksiażki - książki o takim id nie ma w bazie!")
            return redirect('aplikacjaKsiazkowa2:lista')
        else:
            form = BookForm(instance=book)
            context = {'form': form, 'book': book}

            return render(request, 'aplikacjaKsiazkowa2/edit.html', context)

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk'] if 'pk' in kwargs else ''
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
        except ValidationError as err:
            messages.error(request, "Błąd aktualizacji ksiażki - podaj poprawne dane! {}".format(err))
            return redirect('aplikacjaKsiazkowa2:edit_book')
        else:
            try:
                book.save()
                messages.success(request, "Zaktualizowano książkę: {}".format(book))
            except IntegrityError as err:
                messages.error(request, "Błąd aktualizacji ksiażki - IntegrityError {}".format(err))
                return redirect('aplikacjaKsiazkowa2:edit_book')
            else:
                return redirect('aplikacjaKsiazkowa2:lista')


class ListBookView(generic.ListView):
    model = Book
    context_object_name = 'books_data'
    template_name = 'aplikacjaKsiazkowa2/lista.html'
    queryset = Book.objects.all()

    def post(self, request):
        title = request.POST.get('title', '')
        author = request.POST.get('author', '')
        language = request.POST.get('language', '')
        d1 = request.POST.get('d1', '')
        d2 = request.POST.get('d2', '')

        # dopracować poniższy pomysł
        for field, method in (("title", "icontains"), ("author", "icontains")):
            books_data = Book.objects.filter(**{f"{field}__{method}": request.POST.get(field, "")})
            # + django filters

        try:
            if title != "":
                books_data = Book.objects.filter(Q(title__icontains=title))
                context = {'books_data': books_data}
                messages.success(request, "Wyszukiwanie po słowie kluczowym: {}".format(title))
                return render(self.request, 'aplikacjaKsiazkowa2/lista.html', context)
            if author != "":
                books_data = Book.objects.filter(Q(author__icontains=author))
                context = {'books_data': books_data}
                messages.success(request, "Wyszukiwanie po słowie kluczowym: {}".format(author))
                return render(self.request, 'aplikacjaKsiazkowa2/lista.html', context)
            if language != "":
                books_data = Book.objects.filter(Q(language__icontains=language))
                context = {'books_data': books_data}
                messages.success(request, "Wyszukiwanie po słowie kluczowym: {}".format(language))
                return render(self.request, 'aplikacjaKsiazkowa2/lista.html', context)
            if d1 != "" and d2 != "":
                books_data = Book.objects.filter(Q(pub_date__range=(d1, d2)))
                context = {'books_data': books_data}
                messages.success(request, "Wyszukiwanie po przedziale dat: {} - {}".format(d1, d2))
                return render(self.request, 'aplikacjaKsiazkowa2/lista.html', context)

        except ValidationError as err:
            messages.error(request, "Wyszukiwanie książek - validationError: {}".format(err))
            print('Validation error w listowaniu wyników {}'.format(err.message))
            return redirect('aplikacjaKsiazkowa2:lista')
        else:
            messages.warning(request, 'Podałeś nieprawidłowe kryteria wyszukiwania!')
            books_data = Book.objects.all()
            context = {'books_data': books_data}
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
                if response.status_code == status.HTTP_200_OK:
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

                        isbn = ''
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
            except IntegrityError as err:
                messages.error(request, "Błąd korzystania z gugleAPI - spróbuj ponownie: {}".format(err))
                return redirect('aplikacjaKsiazkowa2:gugle')
            except ValidationError as err:
                messages.error(request, "Błąd korzystania z gugleAPI - spróbuj ponownie: {}".format(err))
                return redirect('aplikacjaKsiazkowa2:gugle')
            else:
                return redirect('aplikacjaKsiazkowa2:lista')
