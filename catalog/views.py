from rest_framework.viewsets import ModelViewSet

from .filters import DiskFilter
from .models import Disk
from .serializers import DiskSerializer


class DiskViewSet(ModelViewSet):
    """
    View que gera as funções responsáveis por atender os endpoints.
    Utiliza o ModelViewSet do DRF, que cria automáticamente os endpoints
    catalogo (lista os CDs em GET, cadastra um CD novo em POST),
    e catalogo/<PK> (recupera um CD em GET, altera o registro em PUT e PATCH e remove em DELETE)
    """
    queryset = Disk.objects.all()
    serializer_class = DiskSerializer
    filterset_class = DiskFilter
