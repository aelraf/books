import django_filters
from aplikacjaKsiazkowa2.models import Book


class BookFilter(django_filters.FilterSet):

    author = django_filters.CharFilter(lookup_expr='icontains')
    pub_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Book
        fields = "__all__"
