from django.db.models import Sum
from django.http import Http404
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from catalog.models import Disk
from client.models import Client

from .filters import OrderFilter
from .models import Booking, Order
from .serializers import OrderSerializer
from .utils import (
    MSG_BOOKING_INVALID,
    MSG_CLIENT_INVALID,
    MSG_DISK_INVALID,
    MSG_RESERVED,
    MSG_SOLD
)


class OrderViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    View que gera as funções responsáveis por atender os endpoints.
    Utiliza o GenericViewset do DRF, que cria os comportamentos base que serão utilizados em ModelViewset (ver os
    outros apps do projeto), mas sem criar endpoints automáticamente.
    Além disso, extende os Mixins de CreateModel, ListModel e RetrieveModel, gerando os endpoints pedido (lista os
    pedidos em GET, cadastra um pedido novo em POST), e catalogo/<PK> (recupera um pedido em GET), sem criar endpoints
    para PUT, PATCH ou DELETE.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_class = OrderFilter


class BookingView(APIView):
    """
    View que inicia o processo de compra. Implementa GET e POST.
    """

    def get(self, request, *args, **kwargs):
        """
        Reserva a quantidade pedida e retorna a sua id
        Implementa as seguintes verificações:
        Se o cliente e o disco existem no banco
        Se existe estoque não reservado suficiente para atender à quantidade pedida
        """
        client_id = int(request.query_params['client'])
        disk_id = int(request.query_params['disk'])
        qtd_booked = int(request.query_params['qtd'])
        try:
            disk = Disk.objects.get(id=disk_id)
            client = Client.objects.get(id=client_id)

            if qtd_booked > disk.quantity:
                return Response(data={'msg': MSG_SOLD})

            reserved = Booking.objects.valid().aggregate(Sum('quantity'))['quantity__sum']
            if not reserved:
                reserved = 0

            if (reserved + qtd_booked) > disk.quantity:
                return Response(data={'msg': MSG_RESERVED})
            else:
                booking = Booking(client=client, disk=disk, quantity=qtd_booked)
                booking.save()
                return Response(data={'booking_id': booking.id, })
        except Client.DoesNotExist:
            raise Http404(MSG_CLIENT_INVALID)
        except Disk.DoesNotExist:
            raise Http404(MSG_DISK_INVALID)

    def post(self, request, *args, **kwargs):
        """
        Gera o pedido, decrementa o estoque e apaga a reserva
        """
        try:
            booking_id = int(request.data['booking_id'])
            booking = Booking.objects.valid().get(id=booking_id)

            client = booking.client
            disk = booking.disk
            qtd_booked = booking.quantity

            booking.delete()

            disk.quantity -= qtd_booked
            disk.save()

            order = Order(client=client, disk=disk, quantity=qtd_booked)
            order.save()

            return Response(data={'order_id': order.id, })
        except Booking.DoesNotExist:
            raise Http404(MSG_BOOKING_INVALID)
