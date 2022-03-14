from django_filters import rest_framework as filters

from .models import Order


class OrderFilter(filters.FilterSet):
    """
    Sistema de filtros dos pedidos.
    Permitem filtragem por cliente e período.
    Utiliza a biblioteca Django-filter, que pode ser diretamente integrada ao DRF e oferece
    prontos diversas ferramentas de filtragem em requisições GET.

    Uso: adicionar ao get como query parameters
    Exemplo: ?date_after=2021-11-30&date_before=2021-12-26
    """
    client = filters.Filter(field_name='client__id')
    date = filters.DateFromToRangeFilter(field_name='date')

    class Meta:
        model = Order
        fields = ['client', 'date', ]
