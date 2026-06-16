"""
Wishlist & Favourite Stores API.
"""
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from wishlist.models import Wishlist, FavoriteStore
from ..serializers.wishlist import WishlistSerializer, FavoriteStoreSerializer
from ..utils import SmallPagination, IsOwnerOrReadOnly


class WishlistViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class   = WishlistSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class   = SmallPagination

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related('product')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteStoreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class   = FavoriteStoreSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class   = SmallPagination

    def get_queryset(self):
        return FavoriteStore.objects.filter(user=self.request.user).select_related('seller')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)