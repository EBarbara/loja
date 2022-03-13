import json

import pytest
from django.urls import reverse
from model_bakery import baker

from ..models import Catalog

pytestmark = pytest.mark.django_db


class TestCatalogoEndpoints:

    def test_list(self, api_client):
        quantity = 5
        baker.make(Catalog, _quantity=quantity)

        url = reverse('api:catalogo-list')
        print(url)
        response = api_client().get(url)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == quantity
