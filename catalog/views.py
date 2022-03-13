from rest_framework.viewsets import ModelViewSet

from .models import Catalog
from .serializers import CatalogSerializer


class CatalogViewSet(ModelViewSet):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
