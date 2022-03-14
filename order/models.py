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
    def valid(self):
        threshold = datetime.now() - timedelta(minutes=30)
        return super().get_queryset().filter(date__gt=threshold)


class Booking(models.Model):
    """
    Modelo de pedidos da loja.
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    disk = models.ForeignKey(Disk, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    objects = BookingManager()
