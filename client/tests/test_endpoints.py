import json

import pytest
from django.urls import reverse
from model_bakery import baker

from ..models import Client

pytestmark = pytest.mark.django_db


def get_base_json(instance):
    base_json = {
        'id': instance.id,
        'first_name': instance.first_name,
        'last_name': instance.last_name,
        'email': instance.email,
        'is_staff': instance.is_staff,
        'is_active': instance.is_active,
        'date_joined': instance.date_joined.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        'last_login': 
            instance.last_login.strftime('%Y-%m-%dT%H:%M:%S.%fZ') 
            if instance.last_login 
            else None,
    }
    return base_json


def get_noid_json(instance):
    base_json = {
        'first_name': instance.first_name,
        'last_name': instance.last_name,
        'email': instance.email,
        'is_staff': instance.is_staff,
        'is_active': instance.is_active,
    }
    return base_json

autogen_attrs = ['id', 'date_joined', 'last_login']


def test_list(api_client):
    quantity = 5
    baker.make(Client, _quantity=quantity)

    url = reverse('cliente-list')
    response = api_client().get(url)

    assert response.status_code == 200
    assert len(response.data) == quantity


def test_create(api_client):
    instance = baker.prepare(Client)
    sent_json = get_noid_json(instance)

    url = reverse('cliente-list')
    response = api_client().post(url, data=sent_json, format='json')

    assert response.status_code == 201
    assert len(response.data) == len(sent_json) + len(autogen_attrs)
    assert response.data.items() >= sent_json.items()
    assert all (k in response.data for k in autogen_attrs)


def test_retrieve(api_client):
    instance = baker.make(Client)
    expected_json = get_base_json(instance)

    url = reverse('cliente-detail', kwargs={'pk': instance.id})
    response = api_client().get(url)

    assert response.status_code == 200
    assert response.data == expected_json


def test_update(api_client):
    instance = baker.make(Client)
    new_instance = baker.prepare(Client)
    sent_json = get_noid_json(new_instance)

    url = reverse('cliente-detail', kwargs={'pk': instance.id})
    response = api_client().put(url, sent_json, format='json')

    assert response.status_code == 200
    assert len(response.data) == len(sent_json) + len(autogen_attrs)
    assert response.data.items() >= sent_json.items()
    assert all (k in response.data for k in autogen_attrs) 


def test_delete(api_client):
    instance = baker.make(Client)

    url = reverse('cliente-detail', kwargs={'pk': instance.id})
    response = api_client().delete(url)

    assert response.status_code == 204
    assert Client.objects.all().count() == 0

# TODO criar um teste para o verbo PATCH
