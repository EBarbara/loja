"""
Testes dos filtros de pedido.

Define uma pequena lista de clientes e pedidos através da fixture filter_history e da ferramenta Model Bakery
(que gera instâncias de modelos aleatórias ou com valores fixados e que podem ser injetadas ou não no banco,
sendo destruídas após a execução da função em que são chamadas)

Cada teste verifica se o endpoint de listagem de pedidos de fato filtra o catálogo pelo atributo checado.
Usa a mesma lógica dos testes de filtro de CDs.
"""
from datetime import datetime
from django.urls import reverse
from freezegun import freeze_time
from model_bakery import baker
import pytest

from client.models import Client
from ..models import Order

pytestmark = pytest.mark.django_db

def post_order_at_time(client, date):
    freezer = freeze_time(date)
    freezer.start()
    order = baker.make(Order, client=client)
    freezer.stop()
    return order

@pytest.fixture
def filter_history():
    client_a = baker.make(Client, id=1)
    client_b = baker.make(Client, id=2)
    order_a = post_order_at_time(client_a, '2021-12-15 00:00:00')
    order_b = post_order_at_time(client_a, '2021-12-01 00:00:00')
    order_c = post_order_at_time(client_b, '2021-10-15 00:00:00')
    history = {
        'client_a': client_a,
        'client_b': client_b,
        'order_a': order_a,
        'order_b': order_b,
        'order_c': order_c,
    }
    return history

def test_filter_client(api_client, filter_history):
    client = filter_history['client_a']
    url = reverse('pedido-list')
    response = api_client().get(url, {'client': client.id})
    assert response.status_code == 200
    assert len(response.data) == 2
    for order in response.data:
        assert order['client'] == client.id
        
def test_filter_period(api_client, filter_history):
    start = '2021-12-01'
    finish = '2021-12-30'
    url = reverse('pedido-list')
    response = api_client().get(url, {'date_after': start, 'date_before': finish})
    assert response.status_code == 200
    assert len(response.data) == 2
    for order in response.data:
        order_date = datetime.strptime(order['date'], '%Y-%m-%dT%H:%M:%SZ')
        assert order_date >= datetime.strptime(start, '%Y-%m-%d')
        assert order_date <= datetime.strptime(finish, '%Y-%m-%d')
