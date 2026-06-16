"""
Product, Category, Brand API views.

GET  /api/v1/products/           – paginated list; filterable & sortable
GET  /api/v1/products/{id}/      – detail
POST /api/v1/products/           – create (admin only)
PUT  /api/v1/products/{id}/      – update (admin only)
DELETE /api/v1/products/{id}/    – delete (admin only)

Query params for /products/:
  q             – full-text search across name & description
  category      – filter by category id
  brand         – filter by brand id
  min_price     – price gte
  max_price     – price lte
  ordering      – one of: price, -price, name, -name, created_at, -created_at
  page          – page number
  page_size     – items per page (max 100)
"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, filters as df

from product_management.models import Product, Category, Brand
from ..serializers.products import (
    ProductListSerializer, ProductDetailSerializer,
    CategorySerializer, BrandSerializer,
)
from ..utils import StandardPagination, SmallPagination, IsAdminOrReadOnly


# ── Custom FilterSets ─────────────────────────────────────────────────────────

class ProductFilter(FilterSet):
    min_price = df.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = df.NumberFilter(field_name='price', lookup_expr='lte')
    category  = df.NumberFilter(field_name='category__id')
    brand     = df.NumberFilter(field_name='brand__id')

    class Meta:
        model  = Product
        fields = ['min_price', 'max_price', 'category', 'brand']


# ── ViewSets ──────────────────────────────────────────────────────────────────

class ProductViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for products.
    Read operations are public; writes require staff/admin.
    """
    queryset = Product.objects.filter(is_active=True).select_related('category', 'brand')
    permission_classes = [IsAdminOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class    = ProductFilter
    search_fields      = ['name', 'description']
    ordering_fields    = ['price', 'name', 'created_at']
    ordering           = ['-created_at']   # default: newest first

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductDetailSerializer

    @action(detail=True, methods=['get'], url_path='reviews')
    def reviews(self, request, pk=None):
        """GET /api/v1/products/{id}/reviews/ – paginated reviews for a product."""
        from reviews.models import Review
        from ..serializers.reviews import ReviewSerializer
        product = self.get_object()
        qs = Review.objects.filter(product=product).select_related('user').order_by('-created_at')
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(ReviewSerializer(page, many=True).data)
        return Response(ReviewSerializer(qs, many=True).data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset           = Category.objects.all()
    serializer_class   = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class   = SmallPagination
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['name']
    ordering_fields    = ['name']
    ordering           = ['name']


class BrandViewSet(viewsets.ModelViewSet):
    queryset           = Brand.objects.all()
    serializer_class   = BrandSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class   = SmallPagination
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['name']
    ordering_fields    = ['name']
    ordering           = ['name']