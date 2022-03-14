from django_filters import rest_framework as filters

from .models import Disk


class DiskFilter(filters.FilterSet):
    """
    Sistema de filtros dos CDs.
    Permitem filtragem por nome, ano, artista ou estilo.
    Utiliza a biblioteca Django-filter, que pode ser diretamente integrada ao DRF e oferece
    prontos diversas ferramentas de filtragem em requisições GET.

    Uso: adicionar ao get como query parameters
    Exemplo: ?artist=Scorpions
    """
    name = filters.CharFilter(field_name='name')
    year = filters.NumberFilter(field_name='release_year')
    artist = filters.CharFilter(field_name='artist')
    style = filters.CharFilter(field_name='style')

    class Meta:
        model = Disk
        fields = ['name', 'style', 'year', 'artist', ]
