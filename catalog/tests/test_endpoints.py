import json

import pytest
from django.urls import reverse
from model_bakery import baker

from ..models import Catalog

pytestmark = pytest.mark.django_db


def get_base_json(instance):
    base_json = {
        'id': instance.id,
        'name': instance.name,
        'artist': instance.artist,
        'release_year': instance.release_year,
        'style': instance.style,
        'quantity': instance.quantity,
    }
    return base_json


def get_noid_json(instance):
    base_json = {
        'name': instance.name,
        'artist': instance.artist,
        'release_year': instance.release_year,
        'style': instance.style,
        'quantity': instance.quantity,
    }
    return base_json

autogen_attrs = ['id', ]


def test_list(api_client):
    quantity = 5
    baker.make(Catalog, _quantity=quantity)

    url = reverse('catalogo-list')
    response = api_client().get(url)

    assert response.status_code == 200
    assert len(response.data) == quantity


def test_create(api_client):
    instance = baker.prepare(Catalog)
    sent_json = get_noid_json(instance)

    url = reverse('catalogo-list')
    response = api_client().post(url, data=sent_json, format='json')

    assert response.status_code == 201
    assert len(response.data) == len(sent_json) + len(autogen_attrs)
    assert response.data.items() >= sent_json.items()
    assert all (k in response.data for k in autogen_attrs)


def test_retrieve(api_client):
    instance = baker.make(Catalog)
    expected_json = get_base_json(instance)

    url = reverse('catalogo-detail', kwargs={'pk': instance.id})
    response = api_client().get(url)

    assert response.status_code == 200
    assert response.data == expected_json


def test_update(api_client):
    instance = baker.make(Catalog)
    new_instance = baker.prepare(Catalog)
    sent_json = get_noid_json(new_instance)

    url = reverse('catalogo-detail', kwargs={'pk': instance.id})
    response = api_client().put(url, sent_json, format='json')

    assert response.status_code == 200
    assert len(response.data) == len(sent_json) + len(autogen_attrs)
    assert response.data.items() >= sent_json.items()
    assert all (k in response.data for k in autogen_attrs)


def test_delete(api_client):
    instance = baker.make(Catalog)

    url = reverse('catalogo-detail', kwargs={'pk': instance.id})
    response = api_client().delete(url)

    assert response.status_code == 204
    assert Catalog.objects.all().count() == 0

# TODO criar um teste para o verbo PATCH
