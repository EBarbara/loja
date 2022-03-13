import pytest
from django.urls import reverse
from model_bakery import baker

from order.models import Order
from client.models import Client
from catalog.models import Disk

pytestmark = pytest.mark.django_db


def get_base_json(instance):
    base_json = {
        'id': instance.id,
        'client': instance.client_id,
        'disk': instance.disk_id,
        'quantity': instance.quantity,
        'date': instance.date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
    }
    return base_json


def get_noid_json(instance):
    base_json = {
        'client': instance.client_id,
        'disk': instance.disk_id,
        'quantity': instance.quantity,
    }
    return base_json

autogen_attrs = ['id', 'date']


def test_list(api_client):
    quantity = 5
    baker.make(Order, _quantity=quantity)

    url = reverse('pedido-list')
    response = api_client().get(url)

    assert response.status_code == 200
    assert len(response.data) == quantity


def test_create(api_client):
    client = baker.make(Client)
    disk = baker.make(Disk)
    instance = baker.prepare(Order, client=client, disk=disk)
    sent_json = get_noid_json(instance)

    url = reverse('pedido-list')
    response = api_client().post(url, data=sent_json, format='json')

    assert response.status_code == 201
    assert len(response.data) == len(sent_json) + len(autogen_attrs)
    assert response.data.items() >= sent_json.items()
    assert all (k in response.data for k in autogen_attrs)


def test_retrieve(api_client):
    instance = baker.make(Order)
    expected_json = get_base_json(instance)

    url = reverse('pedido-detail', kwargs={'pk': instance.id})
    response = api_client().get(url)

    assert response.status_code == 200
    assert response.data == expected_json


def test_update(api_client):
    client = baker.make(Client)
    disk = baker.make(Disk)
    instance = baker.make(Order, client=client, disk=disk)
    new_instance = baker.prepare(Order, client=client, disk=disk)
    sent_json = get_noid_json(new_instance)

    url = reverse('pedido-detail', kwargs={'pk': instance.id})
    response = api_client().put(url, sent_json, format='json')

    assert response.status_code == 200
    assert len(response.data) == len(sent_json) + len(autogen_attrs)
    assert response.data.items() >= sent_json.items()
    assert all (k in response.data for k in autogen_attrs) 


def test_delete(api_client):
    instance = baker.make(Order)

    url = reverse('pedido-detail', kwargs={'pk': instance.id})
    response = api_client().delete(url)

    assert response.status_code == 204
    assert Order.objects.all().count() == 0

# TODO criar um teste para o verbo PATCH
