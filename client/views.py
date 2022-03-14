from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Client
from .serializers import ClientSerializer


class ClientViewSet(ModelViewSet):
    """
    View que gera as funções responsáveis por atender os endpoints.
    Utiliza o ModelViewSet do DRF, assim como o ViewSet de CDs.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def destroy(self, request, *args, **kwargs):
        """
        Sobrepõe ao método destroy de ModelViewSet (que é chamado ao acessar o verbo DELETE com o endpoint de
        detalhamento por PK).
        Substitui o Hard Delete (remoção do registro da entidade do banco) por Soft Delete (alteração de uma flag,
        is_active no caso, para indicar que o cliente não está ativo.)
        Retorna HTTP 200 em vez de 204 como o método da classe mãe.
        """
        client = self.get_object()
        client.is_active = False
        client.save()
        return Response(data='Client deleted')
