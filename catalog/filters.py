from django_filters import rest_framework as filters

from .models import Disk


class DiskFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name')
    year = filters.NumberFilter(field_name='release_year')
    artist = filters.CharFilter(field_name='artist')
    style = filters.CharFilter(field_name='style')

    class Meta:
        model = Disk
        fields = ['name', 'style', 'year', 'artist', ]
