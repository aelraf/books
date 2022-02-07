# -*- coding: utf-8 -*-

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def get_route(request):
    routes = [
        'GET /api',
        'GET /api/books',
        'GET /api/books/:id'
    ]
    return Response(routes)
