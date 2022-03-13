from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ClientViewSet

router = DefaultRouter()
router.register(r'cliente', ClientViewSet, basename='cliente')

urlpatterns = [
    path('', include(router.urls)),
]
