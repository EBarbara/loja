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
        'cpf': instance.cpf,
        'email': instance.email,
        'birthday': instance.birthday.strftime('%Y-%m-%d'),
        'is_active': instance.is_active,
    }
    return base_json


def get_noid_json(instance):
    base_json = {
        'first_name': instance.first_name,
        'last_name': instance.last_name,
        'cpf': instance.cpf,
        'email': instance.email,
        'birthday': instance.birthday.strftime('%Y-%m-%d'),
        'is_active': instance.is_active,
    }
    return base_json

autogen_attrs = ['id', ]


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
    instance = baker.make(Client, is_active=True)
    assert instance.is_active == True

    url = reverse('cliente-detail', kwargs={'pk': instance.id})
    response = api_client().delete(url)

    assert response.status_code == 200
    try:
        deleted = Client.objects.get(pk=instance.id)
        assert deleted.is_active == False
    except Client.DoesNotExist:
        pytest.fail(reason="Object was hard removed")


# TODO criar um teste para o verbo PATCH
