# -*- coding: utf-8 -*-

from django.urls import path
from . import views


urlpatterns = [
    path('api', views.get_route),
    path('api/books', views.get_books),
    path('api/books/<str:pk>', views.get_book),
]
