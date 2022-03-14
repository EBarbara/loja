"""
Testes dos endpoints CRUD de catalogo.
Utiliza a fixture api_client (definida no conftest.py da raiz do projeto)
para abrir um cliente do DRF e chamar a combinação endpoint/verbo equivalente
à operação.
As instâncias dos modelos para os testes são gerados via ModelBakery, localmente, de modo a
não ser necessário procurar em vários arquivos onde estão as receitas.

As funções get_base_data e get_noid_data provavelmente poderiam ser fixtures, mas demandariam
muito mais complexidade para receber uma instância como parâmetro.

A lista autogen_attrs se refere aos atributos gerados automaticamente ao criar a instância
e que NÃO fazem parte dos requests e responses dos verbos POST, PUT e PATCH.

Como o TO-DO no final do arquivo mostra, não consegui montar um teste simples de PATCH, delegando
toda a sua função para PUT. Teoricamente, estou testando algo já testado, já que somente uso os métodos
padrão do DRF, mas na prática, ainda há muito espaço para bugs ao chamá-los.
"""
import pytest
from django.urls import reverse
from model_bakery import baker

from ..models import Disk

pytestmark = pytest.mark.django_db


def get_base_data(instance):
    data = {
        'id': instance.id,
        'name': instance.name,
        'artist': instance.artist,
        'release_year': instance.release_year,
        'style': instance.style,
        'quantity': instance.quantity,
        'is_active': instance.is_active,
    }
    return data


def get_noid_data(instance):
    data = {
        'name': instance.name,
        'artist': instance.artist,
        'release_year': instance.release_year,
        'style': instance.style,
        'quantity': instance.quantity,
        'is_active': instance.is_active,
    }
    return data


autogen_attrs = ['id', ]


def test_list(api_client):
    """
    Testa se a resposta é HTTP 200, e se todos os
    elementos da tabela são retornados na chamada
    """
    quantity = 5
    baker.make(Disk, _quantity=quantity)

    url = reverse('catalogo-list')
    response = api_client().get(url)

    assert response.status_code == 200
    assert len(response.data) == quantity


def test_create(api_client):
    """
    Testa se a resposta é HTTP 201, e se instância
    criada é a mesma que deveria ter sido criada.
    Faz alguns malabarismos para verificar se a resposta
    contém os dados passados (extraídos da instância por get_noid_data)
    e também as chaves de autogen_attrs (só as chaves, já que os valores
    foram gerados automaticamente e não sabemos a priori quais são.
    """
    instance = baker.prepare(Disk)
    sent_json = get_noid_data(instance)

    url = reverse('catalogo-list')
    response = api_client().post(url, data=sent_json, format='json')

    assert response.status_code == 201
    assert len(response.data) == len(sent_json) + len(autogen_attrs)
    assert response.data.items() >= sent_json.items()
    assert all(k in response.data for k in autogen_attrs)


def test_retrieve(api_client):
    """
    Testa se a resposta é HTTP 200, e se instância
    obtida é exatamente igual à gerada para o teste.
    """
    instance = baker.make(Disk)
    expected_json = get_base_data(instance)

    url = reverse('catalogo-detail', kwargs={'pk': instance.id})
    response = api_client().get(url)

    assert response.status_code == 200
    assert response.data == expected_json


def test_update(api_client):
    """
    Testa se a resposta é HTTP 200, e se a instância
    após atualizada tem os novos valores que foram passados.
    Segue a mesma idéia de test_create para verificar os
    atributos gerados automaticamente.
    """
    instance = baker.make(Disk)
    new_instance = baker.prepare(Disk)
    sent_json = get_noid_data(new_instance)

    url = reverse('catalogo-detail', kwargs={'pk': instance.id})
    response = api_client().put(url, sent_json, format='json')

    assert response.status_code == 200
    assert len(response.data) == len(sent_json) + len(autogen_attrs)
    assert response.data.items() >= sent_json.items()
    assert all(k in response.data for k in autogen_attrs)


def test_delete(api_client):
    """
    Testa se a resposta é HTTP 204, e se o modelo possui
    uma instância a menos após a remoção.
    """
    instance = baker.make(Disk)

    url = reverse('catalogo-detail', kwargs={'pk': instance.id})
    response = api_client().delete(url)

    assert response.status_code == 204
    assert Disk.objects.all().count() == 0

# TODO criar um teste para o verbo PATCH
