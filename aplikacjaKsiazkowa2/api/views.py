# -*- coding: utf-8 -*-

from django.http import JsonResponse


def get_route(request):
    routes = [
        'GET /api',
        'GET /api/books',
        'GET /api/books/:id'
    ]
    return JsonResponse(routes, safe=False)
