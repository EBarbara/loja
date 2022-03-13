from rest_framework.serializers import ModelSerializer
from .models import Catalog


class CatalogSerializer(ModelSerializer):
    class Meta:
        model = Catalog
        fields = '__all__'
