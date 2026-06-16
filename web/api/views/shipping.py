"""Shipping & Logistics API."""
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from shipping_and_logistics.models import ShippingAddress, ShippingProvider, OrderTracking
from ..serializers.shipping import (
    ShippingAddressSerializer, ShippingProviderSerializer, OrderTrackingSerializer
)
from ..utils import SmallPagination, IsOwnerOrReadOnly, IsAdminOrReadOnly


class ShippingAddressViewSet(viewsets.ModelViewSet):
    serializer_class   = ShippingAddressSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class   = SmallPagination

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ShippingProviderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset           = ShippingProvider.objects.all()
    serializer_class   = ShippingProviderSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class   = SmallPagination


class OrderTrackingViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class   = OrderTrackingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderTracking.objects.filter(order__user=self.request.user).select_related('order')