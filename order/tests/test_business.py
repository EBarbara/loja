"""
Testes da lógica de negócios
Testa funcionalidades diferentes do crud/filtro básico, referentes a regras de negócios
Usa como fixtures locais um cd em situações de estoque cheio e vazio, e um cliente genérico
"""
from datetime import timedelta

import pytest
from django.db.models import Sum
from django.urls import reverse
from freezegun import freeze_time
from model_bakery import baker

from catalog.models import Disk
from client.models import Client
from ..models import Booking, Order
from ..utils import MSG_RESERVED, MSG_SOLD

pytestmark = pytest.mark.django_db


@pytest.fixture
def client():
    client = baker.make(Client)
    return client


@pytest.fixture
def disk():
    disk = baker.make(
        Disk,
        name='We are Reactive',
        artist='Hohpe',
        release_year=2022,
        style='Indie',
        quantity=500,
    )
    return disk


@pytest.fixture
def disk_sold():
    disk = baker.make(
        Disk,
        name='We are Reactive',
        artist='Hohpe',
        release_year=2022,
        style='Indie',
        quantity=2,
    )
    return disk


@pytest.fixture
def bookings_full():
    baker.make(Booking, quantity=400)
    baker.make(Booking, quantity=98)


def test_booking_ok(api_client, client, disk):
    """
    Testa se a resposta ao início do pedido é 200, 
    se a id da reserva foi retornada ao front para finalizar
    e se a reserva correta foi feita.
    """
    quantity_ordered = 2
    data = {
        'disk': disk.id,
        'client': client.id,
        'qtd': quantity_ordered
    }
    url = reverse('fazer_pedido')
    response = api_client().get(url, data)
    assert response.status_code == 200

    try:
        booking_id = response.data['booking_id']
        booking = Booking.objects.valid().get(id=booking_id)
        assert booking.disk.id == disk.id
        assert booking.client.id == client.id
        assert booking.quantity == quantity_ordered
    except KeyError:
        pytest.fail('Mensagem não contém id da reserva')
    except Booking.DoesNotExist:
        pytest.fail('Falha ao criar a reserva')


def test_booking_full(api_client, client, disk, bookings_full):
    """
    Testa se a resposta ao início do pedido é 200,
    se a reserva NÃO foi feita, 
    e se o front é avisado que todos os discos estão reservados.
    A fixture bookings_full não é usada diretamente, mas é necessária
    para garantir que o banco tenha uma reserva quase igual ao estoque
    """
    quantity_ordered = 10
    data = {
        'disk': disk.id,
        'client': client.id,
        'qtd': quantity_ordered
    }
    url = reverse('fazer_pedido')
    response = api_client().get(url, data)
    assert response.status_code == 200
    assert response.data == {'msg': MSG_RESERVED}

    reserved = Booking.objects.valid().aggregate(Sum('quantity'))['quantity__sum']
    assert reserved == 498


def test_booking_sold(api_client, client, disk_sold):
    """
    Testa se a resposta ao início do pedido é 200,
    se a reserva NÃO foi feita, 
    e se o front é avisado que todos os discos estão vendidos.
    """
    quantity_ordered = 10
    data = {
        'disk': disk_sold.id,
        'client': client.id,
        'qtd': quantity_ordered
    }
    url = reverse('fazer_pedido')
    response = api_client().get(url, data)
    assert response.status_code == 200
    assert response.data == {'msg': MSG_SOLD}

    reserved = Booking.objects.valid().aggregate(Sum('quantity'))['quantity__sum']
    assert reserved == None


def test_finish_order(api_client, client, disk):
    """
    Testa se o pedido foi criado, se a reserva foi apagada, 
    e se o front recebeu o pedido.
    """
    quantity_ordered = 2
    booking = baker.make(Booking, client=client, disk=disk, quantity=quantity_ordered)
    inventory_before = Disk.objects.get(id=disk.id).quantity
    data = {'booking_id': booking.id, }

    url = reverse('fazer_pedido')
    response = api_client().post(url, data)
    assert response.status_code == 200

    assert not Booking.objects.filter(id=booking.id).exists()

    inventory_after = Disk.objects.get(id=disk.id).quantity
    assert inventory_after == inventory_before - quantity_ordered

    order_id = response.data['order_id']
    try:
        order = Order.objects.get(id=order_id)
        assert order.disk.id == disk.id
        assert order.client.id == client.id
        assert order.quantity == quantity_ordered
    except KeyError:
        pytest.fail('Mensagem não contém id do pedido')
    except Order.DoesNotExist:
        pytest.fail('Falha ao criar o pedido')


def test_booking_cancel(api_client, client, disk):
    """
    Testa a validade de uma reserva baseado no tempo de criação
    A validade é verificada no queryset "valid", que deve retornar
    somente reservas com menos de 30 min de idade
    """
    booking = baker.make(Booking)
    booking_id = booking.id
    booking_time = booking.date

    # 29 minutos após a criação
    min29 = booking_time + timedelta(minutes=29)
    with freeze_time(min29):
        booking_valid = Booking.objects.valid().filter(id=booking_id).first()
        assert booking_valid

    # 30 minutos após a criação
    min30 = booking_time + timedelta(minutes=30)
    with freeze_time(min30):
        booking_valid = Booking.objects.valid().filter(id=booking_id).first()
        assert not booking_valid

    # 1 ano após a criação
    year = booking_time + timedelta(days=365)
    with freeze_time(year):
        booking_valid = Booking.objects.valid().filter(id=booking_id).first()
        assert not booking_valid
