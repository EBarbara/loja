from django_filters import rest_framework as filters

from .models import Order


class OrderFilter(filters.FilterSet):
    client = filters.Filter(field_name='client__id')
    date = filters.DateFromToRangeFilter(field_name='date')

    class Meta:
        model = Order
        fields = ['client', 'date', ]
