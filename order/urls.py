from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BookingView, OrderViewSet

router = DefaultRouter()
router.register(r'crud', OrderViewSet, basename='pedido')

urlpatterns = [
    path('', include(router.urls)),
    path('compra', BookingView.as_view(), name='fazer_pedido'),
]
