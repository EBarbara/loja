from rest_framework.viewsets import ModelViewSet

from .filters import DiskFilter
from .models import Disk
from .serializers import DiskSerializer


class DiskViewSet(ModelViewSet):
    queryset = Disk.objects.all()
    serializer_class = DiskSerializer
    filterset_class = DiskFilter
