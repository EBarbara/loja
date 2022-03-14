from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from .filters import OrderFilter
from .models import Order
from .serializers import OrderSerializer


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
