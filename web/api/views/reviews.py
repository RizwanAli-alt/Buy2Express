"""
Reviews API.

GET    /api/v1/reviews/?product=<id>  – list reviews for a product
POST   /api/v1/reviews/               – create review (auth required)
DELETE /api/v1/reviews/{id}/          – delete own review
"""
from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Review
from ..serializers.reviews import ReviewSerializer
from ..utils import StandardPagination, IsOwnerOrReadOnly


class ReviewViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class   = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [filters.OrderingFilter]
    ordering_fields    = ['created_at', 'rating']
    ordering           = ['-created_at']

    def get_queryset(self):
        qs = Review.objects.select_related('user', 'product')
        product_id = self.request.query_params.get('product')
        if product_id:
            qs = qs.filter(product_id=product_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)