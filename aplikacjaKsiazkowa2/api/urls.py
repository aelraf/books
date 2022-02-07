# -*- coding: utf-8 -*-

from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_route),
    path('books', views.get_books),
    path('books/<str:pk>', views.get_book),
]