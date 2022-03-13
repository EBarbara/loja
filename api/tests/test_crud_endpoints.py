import json

import pytest
from django.urls import reverse
from model_bakery import baker

from ..models import Catalog

pytestmark = pytest.mark.django_db

modelos_crud = [
    (Catalog, 'api:catalogo-list', 'api:catalogo-detail'),
]


def get_base_json(instance):
    fields = instance._meta.get_fields()
    base_json = {f.name: f.value_from_object(instance) for f in fields}
    return base_json


def get_noid_json(instance):
    base_json = get_base_json(instance)
    return {key: base_json[key] for key in base_json if key != 'id'}


@pytest.mark.parametrize('test_class,list_endpoint,detail_endpoint', modelos_crud)
class TestCrud:

    def test_list(self, api_client, test_class, list_endpoint, detail_endpoint):
        quantity = 5
        baker.make(test_class, _quantity=quantity)

        url = reverse(list_endpoint)
        response = api_client().get(url)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == quantity

    def test_create(self, api_client, test_class, list_endpoint, detail_endpoint):
        instance = baker.prepare(test_class)
        sent_json = get_noid_json(instance)

        url = reverse(list_endpoint)
        response = api_client().post(url, data=sent_json, format='json')
        received_json = json.loads(response.content)

        assert response.status_code == 201
        assert len(received_json) == len(sent_json) + 1
        assert received_json.items() >= sent_json.items()
        assert 'id' in received_json

    def test_retrieve(self, api_client, test_class, list_endpoint, detail_endpoint):
        instance = baker.make(test_class)
        expected_json = get_base_json(instance)

        url = reverse(detail_endpoint, kwargs={'pk': instance.id})
        response = api_client().get(url)

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_update(self, api_client, test_class, list_endpoint, detail_endpoint):
        instance = baker.make(test_class)
        new_instance = baker.prepare(test_class)
        sent_json = get_noid_json(new_instance)

        url = reverse(detail_endpoint, kwargs={'pk': instance.id})
        response = api_client().put(url, sent_json, format='json')
        received_json = json.loads(response.content)

        assert response.status_code == 200
        assert len(received_json) == len(sent_json) + 1
        assert received_json.items() >= sent_json.items()
        assert 'id' in received_json

    def test_delete(self, api_client, test_class, list_endpoint, detail_endpoint):
        instance = baker.make(test_class)

        url = reverse(detail_endpoint, kwargs={'pk': instance.id})
        response = api_client().delete(url)

        assert response.status_code == 204
        assert test_class.objects.all().count() == 0

    # TODO criar um teste genérico para o verbo PATCH
