from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CatalogViewSet

router = DefaultRouter()
router.register(r'catalogo', CatalogViewSet, basename='catalogo')

urlpatterns = [
    path('', include(router.urls)),
]
