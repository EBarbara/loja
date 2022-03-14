from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DiskViewSet

router = DefaultRouter()
router.register(r'crud', DiskViewSet, basename='catalogo')

urlpatterns = [
    path('', include(router.urls)),
]
