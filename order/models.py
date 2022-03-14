from datetime import datetime, timedelta, timezone
from django.db import models

from catalog.models import Disk
from client.models import Client


class Order(models.Model):
    """
    Modelo de pedidos da loja.
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    disk = models.ForeignKey(Disk, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)


class BookingManager(models.Manager):
    """
    Gerenciador de querysets de Booking.
    Tem como função deixar pré implementado o queryset "valid",
    que categoriza como inválidas reservas de 30 minutos ou mais de idade. 
    """
    def valid(self):
        threshold = datetime.now() - timedelta(minutes=30)
        return super().get_queryset().filter(date__gt=threshold)


class Booking(models.Model):
    """
    Modelo de reservas da loja.
    Criado para garantir que um cliente que inicie uma compra não terá problemas com estoque vazio.
    Não possui serializador, pois não é exposto diretamente via endpoint.
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    disk = models.ForeignKey(Disk, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    objects = BookingManager()
