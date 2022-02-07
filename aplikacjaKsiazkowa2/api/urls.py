# -*- coding: utf-8 -*-

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    path('api', views.get_route),
    # path('api/books', views.get_books),
    # path('api/books/<str:pk>', views.get_book),
    path('api/books', views.BookListApi.as_view()),
    path('api/books/<str:pk>', views.BookDetailApi.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
