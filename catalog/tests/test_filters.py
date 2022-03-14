"""
Testes dos filtros de catalogo.

Define um pequeno catálogo de CDs através da fixture filter_catalog e da ferramenta Model Bakery
(que gera instâncias de modelos aleatórias ou com valores fixados e que podem ser injetadas ou não no banco,
sendo destruídas após a execução da função em que são chamadas)

Cada teste verifica se o endpoint de listagem de CDs (o único que faz sentido a aplicação de filtros) de fato
filtra o catálogo pelo atributo checado (Verificando se a lista foi reduzida ao número correto de elementos e
se todos os elementos possuem o campo dentro das especificações do filtro).
"""
from django.urls import reverse
from model_bakery import baker
import pytest

from ..models import Disk

pytestmark = pytest.mark.django_db


@pytest.fixture
def filter_catalog():
    catalog = {
        'disk_a': baker.make(Disk, name='Abbey Road', artist='The Beatles', release_year='1969', style='Rock'),
        'disk_b': baker.make(Disk, name='Let it Be', artist='The Beatles', release_year='1970', style='Rock'),
        'disk_c': baker.make(Disk, name='Morrison Hotel', artist='The Doors', release_year='1970', style='Blues Rock'),
        'disk_d': baker.make(Disk, name='Master of Puppets', artist='Metallica', release_year='1986',
                             style='Heavy Metal'),
        'disk_e': baker.make(Disk, name='Painkiller', artist='Judas Priest', release_year='1990', style='Heavy Metal'),
    }
    return catalog


def test_filter_style(api_client, filter_catalog):
    style = 'Heavy Metal'
    url = reverse('catalogo-list')
    response = api_client().get(url, {'style': style})
    assert response.status_code == 200
    assert len(response.data) == 2
    for disk in response.data:
        assert disk['style'] == style


def test_filter_year(api_client, filter_catalog):
    year = 1970
    url = reverse('catalogo-list')
    response = api_client().get(url, {'year': year})
    assert response.status_code == 200
    assert len(response.data) == 2
    for disk in response.data:
        assert disk['release_year'] == year


def test_filter_artist(api_client, filter_catalog):
    artist = 'The Beatles'
    url = reverse('catalogo-list')
    response = api_client().get(url, {'artist': artist})
    assert response.status_code == 200
    assert len(response.data) == 2
    for disk in response.data:
        assert disk['artist'] == artist


def test_filter_name(api_client, filter_catalog):
    name = 'Morrison Hotel'
    url = reverse('catalogo-list')
    response = api_client().get(url, {'name': name})
    assert response.status_code == 200
    assert len(response.data) == 1
    for disk in response.data:
        assert disk['name'] == name
