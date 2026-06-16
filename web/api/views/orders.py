"""
Orders API.

GET  /api/v1/orders/       – list current user's orders (paginated, newest first)
GET  /api/v1/orders/{id}/  – order detail (user must own it)
"""
from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticated

from cart_and_orders.models import Order
from ..serializers.orders import OrderListSerializer, OrderDetailSerializer
from ..utils import StandardPagination, IsOwnerOrReadOnly


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Read-only viewset scoped to the authenticated user."""
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [filters.OrderingFilter]
    ordering_fields    = ['created_at', 'total_price', 'status']
    ordering           = ['-created_at']

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderListSerializer