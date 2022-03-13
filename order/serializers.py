from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from catalog.models import Disk
from client.models import Client
from .models import Order


class OrderSerializer(ModelSerializer):
    client = PrimaryKeyRelatedField(queryset=Client.objects.all())
    disk = PrimaryKeyRelatedField(queryset=Disk.objects.all())

    class Meta:
        model = Order
        fields = [
            'id',
            'client',
            'disk',
            'quantity',
            'date',
        ]
