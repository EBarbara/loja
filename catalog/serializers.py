from rest_framework.serializers import ModelSerializer
from .models import Disk


class DiskSerializer(ModelSerializer):
    class Meta:
        model = Disk
        fields = '__all__'
