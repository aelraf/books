# -*- coding: utf-8 -*-
from django.forms import ModelForm

from aplikacjaKsiazkowa2.models import Book


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        exclude = ['id']
