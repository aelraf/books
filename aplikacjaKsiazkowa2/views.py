# -*- coding: utf-8 -*-
import datetime

import requests
# from django.core import serializers
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
# from django.http import HttpResponseRedirect
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.dateparse import parse_date
# from django.utils.datetime_safe import date
from django.views import generic, View
from django.views.generic import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status

from aplikacjaKsiazkowa2.models import Book, Publisher, Author
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


""" testowe widoki do sprawdzenia idei - na podstawie dokumentacji"""


class PublisherListView(generic.ListView):
    model = Publisher
    context_object_name = 'my_favorite_publishers'


# https://docs.djangoproject.com/pl/4.0/ref/class-based-views/
# https://docs.djangoproject.com/pl/4.0/topics/class-based-views/intro/
# https://docs.djangoproject.com/pl/4.0/topics/db/queries/
# https://docs.djangoproject.com/pl/3.2/topics/class-based-views/mixins/
# do tego
# https://docs.djangoproject.com/pl/3.2/topics/class-based-views/mixins/#more-than-just-html

class PublisherDetailView(generic.DetailView):
    model = Publisher
    context_object_name = 'publisher'
    queryset = Publisher.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_list'] = Book.objects.all()
        return context


# druga wersja, inne podejście
class PublisherDetailView2(SingleObjectMixin, generic.ListView):
    paginate_by = 2
    template_name = "books/publisher_detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Publisher.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publisher'] = self.object
        return context

    def get_queryset(self):
        return self.object.book_set.all()


class BookListView(generic.ListView):
    queryset = Book.objects.order_by('-pub_date')
    context_object_name = 'book_list'


class AcmeBookListView(generic.ListView):
    context_object_name = 'book_list'
    queryset = Book.objects.filter(publisher__name='ACME Publishing')
    template_name = 'books/acme_list.html'


class PublisherBookListView(generic.ListView):
    template_name = 'books/books_by_publisher.html'

    def get_queryset(self):
        self.publisher = get_object_or_404(Publisher, name=self.kwargs['publisher'])
        return Book.objects.filter(publisher=self.publisher)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publisher'] = self.publisher

        return context


class AuthorDetailView(generic.DetailView):
    queryset = Author.objects.all()

    def get_object(self):
        obj = super().get_object()

        obj.last_accessed = timezone.now()
        obj.save()
        return obj


# drugie podejście do powyższej klasy
class AuthorInterestForm(forms.Form):
    message = forms.CharField()


class AuthorDetailView2(FormMixin, generic.DetailView):
    model = Author
    form_class = AuthorInterestForm

    def get_success_url(self):
        return reverse('author-detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """
        tutaj możemy zapisywać zainteresowania użytkownika używając wiadomości
        przekazywanych w form.cleaned_data['message']
        """
        return super().form_valid(form)


# trzecie podejście
class AuthorDetailView3(generic.DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AuthorInterestForm()
        return context


class AuthorInterestFormView(SingleObjectMixin, FormView):
    template_name = 'books/author_detail.html'
    form_class = AuthorInterestForm
    model = Author

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('author-detail', kwargs={'pk': self.object.pk})


class AuthorView(View):

    def get(self, request, *args, **kwargs):
        view = AuthorDetailView3.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = AuthorInterestFormView.as_view()
        return view(request, *args, **kwargs)


class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # wysyłamy maila używając słownika self.cleaned_data
        pass


class ContactFormView(FormView):
    """lepsza wersja powyższego formularza kontaktowego """
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # ta metoda jest wywoływana, kiedy są POSTowane poprawne dane
        form.send_email()
        return super().form_valid(form)

# poniższe trzy klasy odpowiadają za tworzenie, aktualizację i usuwanie autorów z bazy
# dokładnie taki sam mechanizm można zastosować do książek
# można też negocjować zawartość z JSONem


class JsonableResponseMixin:
    """
    Mixin do dodawania wsparcia JSON do formularza.
    Musi być używane z FormView opartym na obiektach (object-based, np CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        # musimy mieć pewność, że wywołujemy metodę "rodzica" form_valid()
        # ponieważ może ona zrobić część procesów (w przypadku CreateView,
        # wywoła form.save())
        response = super().form_valid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            data = {'pk': self.object.pk, }
            return JsonResponse(data)


class AuthorCreateView(LoginRequiredMixin, CreateView):
    # możemy też użyć tej klasy z odwołaniem do JSONa
    # class AuthorCreateView(JsonableResponseMixin, CreateView):
    model = Author
    fields = ['name']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class AuthorUpdateView(UpdateView):
    model = Author
    fields = ['name']


class AuthorDeleteView(DeleteView):
    model = Author
    success_url = reverse_lazy('author-list')


class RecordInterestView(SingleObjectMixin, View):
    """ rejestruje zainteresowanie bieżącego użytkownika autorem """
    model = Author

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        # patrzymy na autora, którym jesteśmy zainteresowani
        self.object = self.get_object()
        # zainteresowanie rejestrujemy tutaj, w linii powyżej
        return HttpResponseRedirect(reverse('author-detail', kwargs={'pk': self.object.pk}))


class JSONResponseMixin:
    """
    Załóżmy, że piszemy API, w którym powinniśmy zwracać JSONa zamiast renderowania HTML.
    Możemy stworzyć klasę mixin do używania we wszystkich widokach, np obsługującą konwersję do JSONa.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Zwraca odpowiedź JSONową, przekształcając "context" na zawartość.
        """
        return JsonResponse(self.get_data(context), **response_kwargs)

    def get_data(self, context):
        """
        Zwraca obiekt serializowany jako JSON przez json.dumps()
        """
        return context


""" koniec testowych widoków """


class EditView(generic.DetailView):
    """ widok generyczny w zamian za widok edit(request, id), lepiej nazwać BookUpdateView """
    model = Book
    context_object_name = "books_data"
    template_name = 'aplikacjaKsiazkowa2/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_data'] = Book.objects.filter(id=id)

        return context

    def get_queryset(self):
        return Book.objects.filter(id=self.id)

    def post(self, request):
        pass


def edit(request, id):
    edytowana = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        # messages.success(request, "POST - Edytujesz książkę o id: {}".format(id))
        title = request.POST.get('title')
        author = request.POST.get('author')
        data = request.POST.get('pub_date')
        isbn = request.POST.get('isbn')
        pages = request.POST.get('pages')
        cover = request.POST.get('cover')
        language = request.POST.get('language')

        if edytowana.title != title:
            edytowana.title = title
        if edytowana.author != author:
            edytowana.author = author
        try:
            if edytowana.pub_date != data:
                edytowana.pub_date = data
        except ValidationError:
            messages.error(request, "Podano zły format daty!")
            print("edit - data: {}".format(edytowana.pub_date))
        if edytowana.isbn != isbn:
            edytowana.isbn = isbn
        try:
            if edytowana.pages != pages:
                edytowana.pages = pages
        except ValidationError:
            messages.error(request, "Podano zły format ilości stron!")
            print("edit - strony: {}".format(edytowana.pages))

        if edytowana.cover != cover:
            edytowana.cover = cover
        if edytowana.language != language:
            edytowana.language = language
        try:
            edytowana.save()
        except ValidationError:
            messages.error(request, "Podano zły format danych!")

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
